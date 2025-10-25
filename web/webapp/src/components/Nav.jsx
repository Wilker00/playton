import LogoutRoundedIcon from "@mui/icons-material/LogoutRounded";
import LoginRoundedIcon from "@mui/icons-material/LoginRounded";
import {
  AppBar,
  Box,
  Button,
  Chip,
  Container,
  Divider,
  Stack,
  Toolbar,
  Typography,
  useMediaQuery,
} from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { NavLink, useLocation } from "react-router-dom";
import { getToken, clearToken } from "../auth";

const links = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/sandbox", label: "Sandbox" },
  { to: "/xai", label: "Explain" },
  { to: "/agents", label: "Agents" },
  { to: "/environment", label: "Environment" },
  { to: "/risk", label: "Risk" },
  { to: "/exchanges", label: "Exchanges" },
  { to: "/monitoring", label: "Monitoring" },
  { to: "/wallet", label: "Wallet" },
  { to: "/settings", label: "Settings" },
  { to: "/docs", label: "Docs" },
];

export default function Nav() {
  const token = getToken();
  const location = useLocation();
  const theme = useTheme();
  const isSmall = useMediaQuery(theme.breakpoints.down("md"));

  if (location.pathname === "/login") {
    return null;
  }

  return (
    <AppBar
      position="sticky"
      color="transparent"
      elevation={0}
      sx={{
        bgcolor: "rgba(255,255,255,0.92)",
        borderBottom: "1px solid",
        borderColor: "divider",
        boxShadow: "0 12px 32px rgba(15, 23, 42, 0.08)",
        backdropFilter: "blur(14px)",
      }}
    >
      <Container maxWidth="xl">
        <Toolbar
          disableGutters
          sx={{
            py: { xs: 1.5, md: 2.5 },
            gap: { xs: 2, md: 3 },
            flexDirection: { xs: "column", md: "row" },
            alignItems: { xs: "flex-start", md: "center" },
            justifyContent: "space-between",
          }}
        >
          <Stack
            direction={{ xs: "column", md: "row" }}
            spacing={{ xs: 1, md: 2.5 }}
            alignItems={{ xs: "flex-start", md: "center" }}
          >
            <Typography variant="h6" fontWeight={700} color="text.primary">
              Institutional MARL Trading
            </Typography>
            <Stack direction="row" spacing={1.2} flexWrap="wrap">
              <Chip
                label="Live Mode Locked"
                color="error"
                variant="outlined"
                sx={{
                  borderColor: "rgba(248, 113, 113, 0.45)",
                  bgcolor: "rgba(248, 113, 113, 0.1)",
                }}
              />
              <Chip
                label="Paper Mode Active"
                color="success"
                sx={{
                  bgcolor: "rgba(22, 163, 74, 0.12)",
                  color: "#047857",
                }}
              />
            </Stack>
          </Stack>
          <Stack direction="row" spacing={1.5} alignItems="center">
            {token ? (
              <Button
                variant="contained"
                color="primary"
                size={isSmall ? "small" : "medium"}
                startIcon={<LogoutRoundedIcon fontSize="small" />}
                onClick={() => {
                  clearToken();
                  window.location.href = "/login";
                }}
              >
                Logout
              </Button>
            ) : (
              <Button
                component={NavLink}
                to="/login"
                variant="contained"
                color="primary"
                size={isSmall ? "small" : "medium"}
                startIcon={<LoginRoundedIcon fontSize="small" />}
              >
                Login
              </Button>
            )}
          </Stack>
        </Toolbar>
        <Divider sx={{ borderColor: "rgba(209, 213, 219, 0.7)" }} />
        <Box
          sx={{
            py: 1.5,
            display: "flex",
            flexWrap: "wrap",
            gap: 1,
          }}
        >
          {links.map((link) => {
            const active = location.pathname.startsWith(link.to);
            return (
              <Button
                key={link.to}
                component={NavLink}
                to={link.to}
                color="primary"
                variant={active ? "contained" : "outlined"}
                size="small"
                sx={{
                  fontWeight: active ? 700 : 500,
                  letterSpacing: 0.2,
                  bgcolor: active ? "primary.main" : "transparent",
                  color: active ? "common.white" : "text.primary",
                }}
              >
                {link.label}
              </Button>
            );
          })}
        </Box>
      </Container>
    </AppBar>
  );
}
