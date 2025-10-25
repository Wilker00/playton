import { useEffect, useState } from "react";
import InsightsRoundedIcon from "@mui/icons-material/InsightsRounded";
import LanRoundedIcon from "@mui/icons-material/LanRounded";
import StorageRoundedIcon from "@mui/icons-material/StorageRounded";
import {
  Alert,
  Box,
  Card,
  CardContent,
  CardHeader,
  Chip,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import Page from "../components/Page";
import { fetchBusStatus, fetchPrometheusMetrics } from "../api";

export default function Monitoring() {
  const [bus, setBus] = useState(null);
  const [metrics, setMetrics] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [busStatus, promMetrics] = await Promise.all([fetchBusStatus(), fetchPrometheusMetrics()]);
        setBus(busStatus);
        setMetrics(promMetrics);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    };
    load();
  }, []);

  return (
    <Page
      title="Monitoring"
      subtitle="System telemetry spans Redis, Ray orchestration, and Prometheus scrape endpoints."
    >
      <Stack spacing={3}>
        {error && <Alert severity="error">{error}</Alert>}
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardHeader
                avatar={<StorageRoundedIcon color="primary" />}
                title="Redis"
                subheader="Lightweight event bus"
              />
              <CardContent>
                {bus ? (
                  <Chip label={bus.redis} color={bus.redis === "ok" ? "success" : "error"} variant="outlined" />
                ) : (
                  <Typography color="text.secondary">Loading Redis status…</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardHeader
                avatar={<LanRoundedIcon color="secondary" />}
                title="Ray Cluster"
                subheader="Distributed training health"
              />
              <CardContent>
                {bus ? (
                  <Chip label={bus.ray} color={bus.ray === "ok" ? "success" : "error"} variant="outlined" />
                ) : (
                  <Typography color="text.secondary">Loading Ray status…</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardHeader
                avatar={<InsightsRoundedIcon color="info" />}
                title="Prometheus"
                subheader="/metrics endpoint snapshot"
              />
              <CardContent>
                <Typography variant="body2" color="text.secondary">
                  Metrics refresh on demand; integrate with Grafana dashboards for persistent observability.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
        <Card>
          <CardHeader title="Prometheus Metrics" />
          <CardContent>
            <Box
              component="pre"
              sx={{
                bgcolor: "#f9fafb",
                color: "text.primary",
                p: 2.5,
                borderRadius: 2,
                border: "1px solid",
                borderColor: "divider",
                maxHeight: 360,
                overflow: "auto",
                fontFamily: "'Fira Code', 'SFMono-Regular', monospace",
              }}
            >
              {metrics}
            </Box>
          </CardContent>
        </Card>
      </Stack>
    </Page>
  );
}
