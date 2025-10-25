import PropTypes from "prop-types";
import { Container, Stack, Typography } from "@mui/material";

export default function Page({ title, subtitle, actions, children, maxWidth = "xl" }) {
  return (
    <Container maxWidth={maxWidth} sx={{ py: { xs: 3, md: 5 } }}>
      <Stack spacing={3}>
        {(title || subtitle || actions) && (
          <Stack
            direction={{ xs: "column", sm: "row" }}
            spacing={2}
            alignItems={{ xs: "flex-start", sm: "center" }}
            justifyContent="space-between"
          >
            <Stack spacing={0.5}>
              {title && (
                <Typography variant="h4" fontWeight={600} color="text.primary">
                  {title}
                </Typography>
              )}
              {subtitle && (
                <Typography variant="body1" color="text.secondary">
                  {subtitle}
                </Typography>
              )}
            </Stack>
            {actions}
          </Stack>
        )}
        {children}
      </Stack>
    </Container>
  );
}

Page.propTypes = {
  title: PropTypes.string,
  subtitle: PropTypes.string,
  actions: PropTypes.node,
  children: PropTypes.node.isRequired,
  maxWidth: PropTypes.oneOfType([PropTypes.string, PropTypes.bool]),
};
