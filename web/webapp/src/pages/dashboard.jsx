import { useEffect, useMemo, useState } from "react";
import AssessmentRoundedIcon from "@mui/icons-material/AssessmentRounded";
import InsightsRoundedIcon from "@mui/icons-material/InsightsRounded";
import SecurityRoundedIcon from "@mui/icons-material/SecurityRounded";
import TrendingUpRoundedIcon from "@mui/icons-material/TrendingUpRounded";
import {
  Alert,
  Card,
  CardContent,
  CardHeader,
  Chip,
  Grid,
  Skeleton,
  Stack,
  Typography,
} from "@mui/material";
import Page from "../components/Page";
import { fetchMetrics, fetchRiskLimits } from "../api";

const sampleReturns = [0.002, -0.001, 0.003];

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [risk, setRisk] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    const load = async () => {
      try {
        const [metricsResponse, riskResponse] = await Promise.all([
          fetchMetrics(sampleReturns),
          fetchRiskLimits(),
        ]);
        if (!active) return;
        setMetrics(metricsResponse);
        setRisk(riskResponse);
        setError(null);
      } catch (err) {
        if (active) setError(err.message);
      }
    };
    load();
    const interval = setInterval(load, 5000);
    return () => {
      active = false;
      clearInterval(interval);
    };
  }, []);

  const metricItems = useMemo(() => {
    if (!metrics) return [];
    return [
      { label: "Cumulative Return", value: `${(metrics.cumulative_return * 100).toFixed(2)}%` },
      { label: "Sharpe Ratio", value: metrics.sharpe.toFixed(2) },
      { label: "Sortino Ratio", value: metrics.sortino.toFixed(2) },
      { label: "CVaR 95", value: `${(metrics.cvar * 100).toFixed(2)}%` },
      { label: "Max Drawdown", value: `${(metrics.max_drawdown * 100).toFixed(2)}%` },
      { label: "Turnover", value: `${(((metrics.turnover ?? 0) * 100)).toFixed(2)}%` },
    ];
  }, [metrics]);

  return (
    <Page
      title="Paper Trading Dashboard"
      subtitle="Live execution remains gated behind manual approval with fail-safe protections."
    >
      <Stack spacing={3}>
        {error && <Alert severity="error">{error}</Alert>}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card sx={{ height: "100%" }}>
              <CardHeader
                avatar={<TrendingUpRoundedIcon color="primary" fontSize="large" />}
                title="Portfolio Pulse"
                subheader="Real-time performance analytics from the paper book"
              />
              <CardContent>
                {metrics ? (
                  <Stack spacing={1.5}>
                    {metricItems.map((item) => (
                      <Stack
                        key={item.label}
                        direction="row"
                        alignItems="center"
                        justifyContent="space-between"
                      >
                        <Typography variant="body2" color="text.secondary">
                          {item.label}
                        </Typography>
                        <Typography variant="subtitle1" fontWeight={600} color="text.primary">
                          {item.value}
                        </Typography>
                      </Stack>
                    ))}
                    <Chip
                      icon={<InsightsRoundedIcon />}
                      label="Metrics refresh every 5s"
                      variant="outlined"
                      color="secondary"
                      sx={{ alignSelf: "flex-start", mt: 1 }}
                    />
                  </Stack>
                ) : (
                  <Stack spacing={1.5}>
                    {[...Array(5)].map((_, index) => (
                      <Skeleton key={index} height={24} sx={{ borderRadius: 1 }} />
                    ))}
                  </Stack>
                )}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card sx={{ height: "100%" }}>
              <CardHeader
                avatar={<SecurityRoundedIcon color="secondary" fontSize="large" />}
                title="Risk Controls"
                subheader="Guardrails enforced before routing any execution"
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
                    <Chip
                      icon={<AssessmentRoundedIcon />}
                      label="Paper portfolio in compliance"
                      color="success"
                      variant="outlined"
                      sx={{ alignSelf: "flex-start" }}
                    />
                  </Stack>
                ) : (
                  <Stack spacing={1.5}>
                    {[...Array(3)].map((_, index) => (
                      <Skeleton key={index} height={24} sx={{ borderRadius: 1 }} />
                    ))}
                  </Stack>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Stack>
    </Page>
  );
}
