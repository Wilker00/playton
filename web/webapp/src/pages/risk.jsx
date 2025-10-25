import { useEffect, useState } from "react";
import BoltRoundedIcon from "@mui/icons-material/BoltRounded";
import GppMaybeRoundedIcon from "@mui/icons-material/GppMaybeRounded";
import HealthAndSafetyRoundedIcon from "@mui/icons-material/HealthAndSafetyRounded";
import WarningRoundedIcon from "@mui/icons-material/WarningRounded";
import {
  Alert,
  Button,
  Card,
  CardContent,
  CardHeader,
  Chip,
  Grid,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import Page from "../components/Page";
import { activateFailSafe, fetchFailSafeStatus, fetchRiskLimits } from "../api";

export default function Risk() {
  const [risk, setRisk] = useState(null);
  const [failSafe, setFailSafe] = useState(null);
  const [error, setError] = useState(null);
  const [reason, setReason] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const load = async () => {
    try {
      const [riskResponse, failSafeResponse] = await Promise.all([fetchRiskLimits(), fetchFailSafeStatus()]);
      setRisk(riskResponse);
      setFailSafe(failSafeResponse);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const triggerFailSafe = async () => {
    try {
      setSubmitting(true);
      await activateFailSafe(reason);
      setReason("");
      await load();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Page
      title="Risk & Controls"
      subtitle="Fail-safe blocks all routing until human reset; defaults to paper execution."
    >
      <Stack spacing={3}>
        {error && <Alert severity="error">{error}</Alert>}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader
                avatar={<HealthAndSafetyRoundedIcon color="primary" />}
                title="Risk Limits"
                subheader="Real-time thresholds applied to orders"
              />
              <CardContent>
                {risk ? (
                  <Stack spacing={2}>
                    <Stack direction="row" justifyContent="space-between" alignItems="center">
                      <Typography variant="body2" color="text.secondary">
                        Max Leverage
                      </Typography>
                      <Typography variant="subtitle1" fontWeight={600}>
                        {risk.max_leverage.toFixed(2)}x
                      </Typography>
                    </Stack>
                    <Stack direction="row" justifyContent="space-between" alignItems="center">
                      <Typography variant="body2" color="text.secondary">
                        Daily Loss Limit
                      </Typography>
                      <Typography variant="subtitle1" fontWeight={600}>
                        {(risk.daily_loss_limit * 100).toFixed(2)}%
                      </Typography>
                    </Stack>
                    <Stack direction="row" justifyContent="space-between" alignItems="center">
                      <Typography variant="body2" color="text.secondary">
                        Kill Switch
                      </Typography>
                      <Chip
                        label={risk.kill_switch ? "Armed" : "Standby"}
                        color={risk.kill_switch ? "error" : "success"}
                        variant={risk.kill_switch ? "filled" : "outlined"}
                      />
                    </Stack>
                  </Stack>
                ) : (
                  <Typography color="text.secondary">Loading risk limits…</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader
                avatar={<WarningRoundedIcon color="error" />}
                title="Fail-Safe"
                subheader="Instant circuit breaker for paper and future live flows"
              />
              <CardContent>
                {failSafe ? (
                  <Stack spacing={2}>
                    <Stack direction="row" spacing={1.5} alignItems="center">
                      <Chip
                        label={failSafe.active ? "ACTIVE" : "IDLE"}
                        color={failSafe.active ? "error" : "success"}
                        variant={failSafe.active ? "filled" : "outlined"}
                      />
                      {failSafe.reason && (
                        <Chip
                          icon={<GppMaybeRoundedIcon />}
                          label={failSafe.reason}
                          color="warning"
                          variant="outlined"
                        />
                      )}
                    </Stack>
                    {failSafe.activated_at && (
                      <Typography variant="body2" color="text.secondary">
                        Activated {new Date(failSafe.activated_at).toLocaleString()}
                      </Typography>
                    )}
                    <Stack direction={{ xs: "column", sm: "row" }} spacing={2} alignItems={{ xs: "stretch", sm: "center" }}>
                      <TextField
                        fullWidth
                        label="Reason"
                        value={reason}
                        onChange={(event) => setReason(event.target.value)}
                        placeholder="Optional reason for audit trail"
                      />
                      <Button
                        variant="contained"
                        color="error"
                        onClick={triggerFailSafe}
                        disabled={submitting}
                        startIcon={<BoltRoundedIcon />}
                        sx={{ borderRadius: 3, whiteSpace: "nowrap" }}
                      >
                        {submitting ? "Activating…" : "Activate Kill Switch"}
                      </Button>
                    </Stack>
                  </Stack>
                ) : (
                  <Typography color="text.secondary">Loading fail-safe status…</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Stack>
    </Page>
  );
}
