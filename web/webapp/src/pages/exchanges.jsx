import { useEffect, useState } from "react";
import CloudDoneRoundedIcon from "@mui/icons-material/CloudDoneRounded";
import CloudOffRoundedIcon from "@mui/icons-material/CloudOffRounded";
import HubRoundedIcon from "@mui/icons-material/HubRounded";
import {
  Alert,
  Card,
  CardContent,
  CardHeader,
  Chip,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import Page from "../components/Page";
import { fetchExchanges } from "../api";

export default function Exchanges() {
  const [exchanges, setExchanges] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const status = await fetchExchanges();
        setExchanges(status);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    };
    load();
  }, []);

  return (
    <Page
      title="Exchange Connectivity"
      subtitle="All adapters remain in paper mode with recorded fixtures and public market data."
    >
      <Stack spacing={3}>
        {error && <Alert severity="error">{error}</Alert>}
        <Grid container spacing={3}>
          {exchanges.map((exchange) => {
            const online = exchange.status === "online";
            return (
              <Grid item xs={12} md={4} key={exchange.exchange}>
                <Card>
                  <CardHeader
                    avatar={<HubRoundedIcon color={online ? "success" : "error"} />}
                    title={exchange.exchange.toUpperCase()}
                    subheader={`Mode: ${exchange.mode}`}
                  />
                  <CardContent>
                    <Stack spacing={2}>
                      <Chip
                        icon={online ? <CloudDoneRoundedIcon /> : <CloudOffRoundedIcon />}
                        label={online ? "Online" : "Offline"}
                        color={online ? "success" : "error"}
                        variant={online ? "filled" : "outlined"}
                      />
                      <Typography variant="body2" color="text.secondary">
                        Connectivity is health-checked every 30 seconds. Paper mode routes to simulated order books with
                        immediate cancellation support.
                      </Typography>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
            );
          })}
        </Grid>
      </Stack>
    </Page>
  );
}
