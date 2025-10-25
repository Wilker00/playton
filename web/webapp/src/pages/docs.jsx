import { useEffect, useState } from "react";
import BookRoundedIcon from "@mui/icons-material/BookRounded";
import TipsAndUpdatesRoundedIcon from "@mui/icons-material/TipsAndUpdatesRounded";
import { Alert, Card, CardContent, CardHeader, Tab, Tabs } from "@mui/material";
import ReactMarkdown from "react-markdown";
import Page from "../components/Page";
import { fetchDocs } from "../api";

export default function Docs() {
  const [docs, setDocs] = useState({ agents: "", readme: "" });
  const [error, setError] = useState(null);
  const [tab, setTab] = useState(0);

  useEffect(() => {
    const load = async () => {
      try {
        const response = await fetchDocs();
        setDocs(response);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    };
    load();
  }, []);

  return (
    <Page title="Documentation" subtitle="Legal, operational, and agent-specific guidelines.">
      <Card>
        <CardHeader
          avatar={tab === 0 ? <TipsAndUpdatesRoundedIcon color="primary" /> : <BookRoundedIcon color="primary" />}
          title={tab === 0 ? "Agent Guidelines" : "README"}
          subheader={tab === 0 ? "Operational guardrails for agents" : "Project overview and runbooks"}
        />
        <CardContent>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <Tabs
            value={tab}
            onChange={(_, value) => setTab(value)}
            textColor="secondary"
            indicatorColor="secondary"
            sx={{ mb: 2 }}
          >
            <Tab label="AGENTS.md" />
            <Tab label="README.md" />
          </Tabs>
          <div style={{ maxHeight: "60vh", overflow: "auto" }}>
            <ReactMarkdown>
              {tab === 0 ? docs.agents : docs.readme}
            </ReactMarkdown>
          </div>
        </CardContent>
      </Card>
    </Page>
  );
}
