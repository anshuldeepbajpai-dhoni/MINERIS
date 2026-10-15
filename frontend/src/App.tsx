import { useState } from "react";

import Login from "./pages/Login";
import Mines from "./pages/Mines";

function App() {
  const [authenticated, setAuthenticated] = useState(
    Boolean(localStorage.getItem("mineris_token"))
  );

  if (!authenticated) {
    return (
      <Login
        onLogin={() => setAuthenticated(true)}
      />
    );
  }

  return (
    <Mines
      onLogout={() => {
        localStorage.removeItem("mineris_token");
        setAuthenticated(false);
      }}
    />
  );
}

export default App;
