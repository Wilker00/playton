import { useState } from "react";
import PaletteRoundedIcon from "@mui/icons-material/PaletteRounded";
import ScheduleRoundedIcon from "@mui/icons-material/ScheduleRounded";
import SavingsRoundedIcon from "@mui/icons-material/SavingsRounded";
import {
  Card,
  CardContent,
  CardHeader,
  Grid,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import Page from "../components/Page";

export default function Settings() {
  const [pollInterval, setPollInterval] = useState(5000);
  const [theme, setTheme] = useState("dark");
  const [sandboxBalance, setSandboxBalance] = useState(100000);

  return (
    <Page
      title="Application Settings"
      subtitle="Local preferences only; no impact on live connectivity or custody."
    >
      <Stack spacing={3}>
        <Grid container spacing={3} maxWidth="md">
          <Grid item xs={12} md={4}>
            <Card>
              <CardHeader
                avatar={<ScheduleRoundedIcon color="primary" />}
                title="Polling"
                subheader="Control UI refresh interval"
              />
              <CardContent>
                <TextField
                  fullWidth
                  type="number"
                  label="Poll Interval (ms)"
                  value={pollInterval}
                  onChange={(event) => setPollInterval(Number(event.target.value))}
                  inputProps={{ min: 1000, step: 500 }}
                />
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardHeader
                avatar={<PaletteRoundedIcon color="secondary" />}
                title="Theme"
                subheader="Preview alternate palettes"
              />
              <CardContent>
                <TextField select fullWidth label="Theme" value={theme} onChange={(event) => setTheme(event.target.value)}>
                  <MenuItem value="dark">Dark</MenuItem>
                  <MenuItem value="light">Light</MenuItem>
                </TextField>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardHeader
                avatar={<SavingsRoundedIcon color="success" />}
                title="Sandbox Balance"
                subheader="Local what-if allocation"
              />
              <CardContent>
                <TextField
                  fullWidth
                  type="number"
                  label="Sandbox Balance (USD)"
                  value={sandboxBalance}
                  onChange={(event) => setSandboxBalance(Number(event.target.value))}
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
        <Card>
          <CardHeader title="Preview" />
          <CardContent>
            <Typography variant="body1">
              Polling every {(pollInterval / 1000).toFixed(1)}s with {theme} theme. Sandbox balance
              {" "}
              {sandboxBalance.toLocaleString()} USD.
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              These preferences persist locally and never modify backend configuration or trading behavior.
            </Typography>
          </CardContent>
        </Card>
      </Stack>
    </Page>
  );
}
