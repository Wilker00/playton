import { useEffect, useMemo, useState } from "react";
import AutorenewRoundedIcon from "@mui/icons-material/AutorenewRounded";
import LandscapeRoundedIcon from "@mui/icons-material/LandscapeRounded";
import TimelineRoundedIcon from "@mui/icons-material/TimelineRounded";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Chip,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import Page from "../components/Page";
import { fetchEnvConfig, fetchRegime } from "../api";

const simulatedRegimes = ["BULL_VOLATILE", "BEAR_STABLE", "SIDEWAYS_CHOPPY"];

export default function Environment() {
  const [envConfig, setEnvConfig] = useState(null);
  const [regime, setRegime] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [envResponse, regimeResponse] = await Promise.all([fetchEnvConfig(), fetchRegime()]);
        setEnvConfig(envResponse);
        setRegime(regimeResponse);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    };
    load();
  }, []);

  const regimeChipColor = useMemo(() => {
    if (!regime) return "default";
    switch (regime.regime) {
      case "BULL_VOLATILE":
        return "success";
      case "BEAR_STABLE":
        return "error";
      case "SIDEWAYS_CHOPPY":
        return "warning";
      default:
        return "info";
    }
  }, [regime]);

  const simulateRegime = () => {
    const next = simulatedRegimes[Math.floor(Math.random() * simulatedRegimes.length)];
    setRegime({ regime: next, confidence: Math.random(), updated_at: new Date().toISOString() });
  };

  return (
    <Page
      title="Environment & Regime"
      subtitle="Training stacks stay in paper mode with regime-aware risk throttling."
    >
      <Stack spacing={3}>
        {error && <Alert severity="error">{error}</Alert>}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader
                avatar={<LandscapeRoundedIcon color="primary" />}
                title="Environment Configuration"
                subheader="Hydra-controlled parameters for the TradingEnv"
              />
              <CardContent>
                {envConfig ? (
                  <Box
                    component="pre"
                    sx={{
                      bgcolor: "#f9fafb",
                      color: "text.primary",
                      borderRadius: 2,
                      p: 2.5,
                      border: "1px solid",
                      borderColor: "divider",
                      fontFamily: "'Fira Code', 'SFMono-Regular', monospace",
                      maxHeight: 360,
                      overflow: "auto",
                    }}
                  >
                    {JSON.stringify(envConfig, null, 2)}
                  </Box>
                ) : (
                  <Typography color="text.secondary">Loading environment configuration…</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card sx={{ height: "100%" }}>
              <CardHeader
                avatar={<TimelineRoundedIcon color="secondary" />}
                title="Detected Regime"
                subheader="Signals drive leverage controls and ensemble weighting"
              />
              <CardContent>
                {regime ? (
                  <Stack spacing={2}>
                    <Stack direction="row" spacing={1.5} alignItems="center">
                      <Chip
                        label={regime.regime}
                        color={regimeChipColor}
                        size="medium"
                        variant="outlined"
                      />
                      <Chip label={`Confidence ${(regime.confidence * 100).toFixed(1)}%`} color="info" variant="outlined" />
                    </Stack>
                    <Typography variant="body2" color="text.secondary">
                      Updated {new Date(regime.updated_at).toLocaleString()}
                    </Typography>
                    <Button
                      variant="contained"
                      color="secondary"
                      startIcon={<AutorenewRoundedIcon />}
                      onClick={simulateRegime}
                      sx={{ alignSelf: "flex-start", borderRadius: 3 }}
                    >
                      Simulate Regime Change
                    </Button>
                  </Stack>
                ) : (
                  <Typography color="text.secondary">Loading regime telemetry…</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Stack>
    </Page>
  );
}
