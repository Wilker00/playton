import React from "react";
import ReactDOM from "react-dom/client";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import { StyledEngineProvider } from "@mui/material/styles";
import "@fontsource/inter/400.css";
import "@fontsource/inter/600.css";
import AppRouter from "./router";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#111827" },
    secondary: { main: "#4c1d95" },
    background: {
      default: "#f4f5f7",
      paper: "#ffffff",
    },
    text: {
      primary: "#111827",
      secondary: "#4b5563",
    },
  },
  typography: {
    fontFamily: "'Inter', 'Segoe UI', sans-serif",
    h4: { fontWeight: 700, letterSpacing: "-0.01em" },
    button: { fontWeight: 600 },
  },
  shape: { borderRadius: 12 },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: "#f4f5f7",
          backgroundImage: "linear-gradient(180deg, #f9fafb 0%, #eef2ff 100%)",
        },
      },
    },
    MuiButton: {
      defaultProps: {
        disableElevation: true,
      },
      styleOverrides: {
        root: {
          borderRadius: 999,
          textTransform: "none",
          fontWeight: 600,
          paddingInline: "1.25rem",
          paddingBlock: "0.6rem",
        },
        containedPrimary: {
          backgroundColor: "#111827",
          color: "#ffffff",
          "&:hover": {
            backgroundColor: "#000000",
          },
        },
        outlinedPrimary: {
          borderColor: "#d1d5db",
          color: "#111827",
          "&:hover": {
            borderColor: "#111827",
            backgroundColor: "rgba(17, 24, 39, 0.06)",
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 20,
          border: "1px solid #e5e7eb",
          boxShadow: "0 18px 40px rgba(15, 23, 42, 0.08)",
          backgroundImage: "none",
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          fontWeight: 600,
          letterSpacing: 0.1,
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
        },
      },
    },
  },
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <StyledEngineProvider injectFirst>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AppRouter />
      </ThemeProvider>
    </StyledEngineProvider>
  </React.StrictMode>
);
