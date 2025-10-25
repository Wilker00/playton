import { useEffect, useMemo, useState } from "react";
import BarChartRoundedIcon from "@mui/icons-material/BarChartRounded";
import InsightsRoundedIcon from "@mui/icons-material/InsightsRounded";
import {
  Alert,
  Card,
  CardContent,
  CardHeader,
  Stack,
  Typography,
  useTheme,
} from "@mui/material";
import Page from "../components/Page";
import { fetchShap } from "../api";

export default function XAI() {
  const [shapValues, setShapValues] = useState({});
  const [error, setError] = useState(null);
  const theme = useTheme();

  useEffect(() => {
    const load = async () => {
      try {
        const response = await fetchShap();
        setShapValues(response);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    };
    load();
  }, []);

  const entries = useMemo(() => Object.entries(shapValues), [shapValues]);
  const maxValue = entries.length > 0 ? Math.max(...entries.map(([, value]) => Math.abs(value)), 1) : 1;

  return (
    <Page
      title="Explainability"
      subtitle="SHAP feature attributions per agent drive human audit trails in paper mode."
    >
      <Stack spacing={3}>
        {error && <Alert severity="error">{error}</Alert>}
        <Card>
          <CardHeader
            avatar={<InsightsRoundedIcon color="secondary" />}
            title="Feature Contributions"
            subheader="Positive (teal) indicates increased weight; negative (pink) reduces weight"
          />
          <CardContent>
            {entries.length > 0 ? (
              <svg width="100%" height={entries.length * 44} viewBox={`0 0 700 ${entries.length * 44}`}>
                {entries.map(([feature, value], index) => {
                  const magnitude = Math.abs(value);
                  const normalized = magnitude / maxValue;
                  const barWidth = normalized * 360;
                  const color = value >= 0 ? theme.palette.secondary.main : theme.palette.error.main;
                  return (
                    <g key={feature} transform={`translate(0, ${index * 44})`}>
                      <text x={0} y={24} fill={theme.palette.text.secondary} style={{ fontSize: "14px" }}>
                        {feature}
                      </text>
                      <rect
                        x={220}
                        y={10}
                        width={barWidth}
                        height={18}
                        fill={color}
                        rx={9}
                        ry={9}
                      />
                      <text x={220 + barWidth + 12} y={24} fill={theme.palette.text.primary} style={{ fontSize: "14px" }}>
                        {value.toFixed(3)}
                      </text>
                    </g>
                  );
                })}
              </svg>
            ) : (
              <Typography color="text.secondary">Loading explainability data…</Typography>
            )}
          </CardContent>
        </Card>
        <Card variant="outlined">
          <CardHeader
            avatar={<BarChartRoundedIcon color="primary" />}
            title="Interpretation"
            subheader="Attributions refresh alongside each evaluation batch"
          />
          <CardContent>
            <Typography variant="body2" color="text.secondary">
              Feature contributions are computed on the paper dataset and inform human approvals for any future live
              trades. Maintain transparency by exporting these charts to MLflow along with VectorBT reports.
            </Typography>
          </CardContent>
        </Card>
      </Stack>
    </Page>
  );
}
