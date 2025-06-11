// pages/index.tsx
// import { Button, Container, Typography } from '@mui/material'
import { useEffect } from "react";
import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.replace("/ResumeGenerator");
  }, [router]);

  return null;
}

// export default function Home() {
//   return (
//     <Container sx={{ py: 4 }}>
//       <Typography variant="h4" gutterBottom>
//         Hello MUI in Next.js!
//       </Typography>
//       <Button variant="contained" color="primary">
//         Click Me
//       </Button>
//     </Container>
//   )
// }
