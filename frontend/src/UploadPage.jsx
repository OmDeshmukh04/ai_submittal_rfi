import React, {useState} from "react";
import axios from "axios";

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
      <button onClick={checkHealth}>Check Backend Health</button>
      <pre>{health}</pre>
    </div>
  );
}
