import { useEffect, useState } from "react";
import KeyRoundedIcon from "@mui/icons-material/KeyRounded";
import LockOpenRoundedIcon from "@mui/icons-material/LockOpenRounded";
import LockPersonRoundedIcon from "@mui/icons-material/LockPersonRounded";
import VerifiedUserRoundedIcon from "@mui/icons-material/VerifiedUserRounded";
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
import { fetchWalletStatus } from "../api";

export default function Wallet() {
  const [wallet, setWallet] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const response = await fetchWalletStatus();
        setWallet(response);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    };
    load();
  }, []);

  return (
    <Page
      title="Wallet Integration"
      subtitle="Client-side signing only. Servers never hold private keys or custody funds."
    >
      <Stack spacing={3}>
        {error && <Alert severity="error">{error}</Alert>}
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardHeader
                avatar={<VerifiedUserRoundedIcon color="primary" />}
                title="Signing"
                subheader="Paper approvals require client signatures"
              />
              <CardContent>
                {wallet ? (
                  <Chip
                    label={wallet.signing_required ? "Required" : "Optional"}
                    color={wallet.signing_required ? "warning" : "success"}
                    variant="outlined"
                  />
                ) : (
                  <Typography color="text.secondary">Loading signing status…</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardHeader
                avatar={<LockPersonRoundedIcon color="secondary" />}
                title="Custody"
                subheader="No private keys on backend infrastructure"
              />
              <CardContent>
                {wallet ? (
                  <Typography variant="subtitle1" fontWeight={600}>
                    {wallet.custody}
                  </Typography>
                ) : (
                  <Typography color="text.secondary">Loading custody status…</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardHeader
                avatar={<KeyRoundedIcon color="info" />}
                title="Connectivity"
                subheader="Paper signer availability"
              />
              <CardContent>
                {wallet ? (
                  <Chip
                    label={wallet.connected ? "Connected" : "Offline"}
                    color={wallet.connected ? "success" : "error"}
                    variant={wallet.connected ? "filled" : "outlined"}
                    icon={<LockOpenRoundedIcon />}
                  />
                ) : (
                  <Typography color="text.secondary">Loading connection status…</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Stack>
    </Page>
  );
}
