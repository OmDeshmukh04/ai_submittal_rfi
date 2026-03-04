import React, { useState } from "react";
import axios from "axios";
import UploadForm from "./UploadForm";

export default function UploadPage(){
  const [health, setHealth] = useState(null);

  const checkHealth = async () => {
    try {
      const res = await axios.get("http://localhost:8000/api/health");
      setHealth(JSON.stringify(res.data));
    } catch (e) {
      setHealth("Backend not reachable");
    }
  };

  return (
    <div>
      <div style={{ marginBottom: 12 }}>
        <button onClick={checkHealth}>Check Backend Health</button>
        <pre>{health}</pre>
      </div>

      <UploadForm />
    </div>
  );
}
