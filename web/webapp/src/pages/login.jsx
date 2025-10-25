import { useState } from "react";
import { useNavigate } from "react-router-dom";
import LoginRoundedIcon from "@mui/icons-material/LoginRounded";
import LockRoundedIcon from "@mui/icons-material/LockRounded";
import PersonRoundedIcon from "@mui/icons-material/PersonRounded";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Container,
  InputAdornment,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { login as loginRequest } from "../api";
import { setToken } from "../auth";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("viewer");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      setLoading(true);
      const response = await loginRequest(username, password, role);
      setToken(response.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        bgcolor: "background.default",
        backgroundImage:
          "radial-gradient(circle at 10% 20%, rgba(148, 163, 184, 0.25), transparent 55%), radial-gradient(circle at 90% 20%, rgba(79, 70, 229, 0.18), transparent 50%)",
        backgroundRepeat: "no-repeat",
        px: 2,
      }}
    >
      <Container maxWidth="sm">
        <Stack spacing={3}>
          <Stack spacing={1} textAlign="center">
            <Typography variant="h4" fontWeight={700} color="text.primary">
              Paper Trading Console
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Authenticate to access the momentum and mean reversion monitoring suite. Live routing stays locked
              until human approval.
            </Typography>
          </Stack>
          <Card>
            <CardHeader
              title="Sign in"
              subheader="Session tokens are stored locally within your browser."
            />
            <CardContent>
              <Stack component="form" spacing={3} onSubmit={handleSubmit}>
                {error && <Alert severity="error">{error}</Alert>}
                <TextField
                  label="Username"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  required
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <PersonRoundedIcon fontSize="small" />
                      </InputAdornment>
                    ),
                  }}
                />
                <TextField
                  label="Password"
                  type="password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <LockRoundedIcon fontSize="small" />
                      </InputAdornment>
                    ),
                  }}
                />
                <TextField
                  select
                  label="Role Scope"
                  value={role}
                  onChange={(event) => setRole(event.target.value)}
                  helperText="Determines JWT scope for backend authorization"
                >
                  <MenuItem value="viewer">Viewer</MenuItem>
                  <MenuItem value="risk">Risk</MenuItem>
                  <MenuItem value="admin">Admin</MenuItem>
                </TextField>
                <Button
                  type="submit"
                  variant="contained"
                  size="large"
                  endIcon={<LoginRoundedIcon />}
                  disabled={loading}
                >
                  {loading ? "Signing in…" : "Sign in"}
                </Button>
              </Stack>
            </CardContent>
          </Card>
        </Stack>
      </Container>
    </Box>
  );
}
