import React, { useState } from "react";
import axios from "axios";

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
  };

  const upload = async () => {
    if (!file) return alert("Choose a PDF file first.");
    const fd = new FormData();
    fd.append("file", file);
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/api/upload/", fd, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Upload failed. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  const runOcr = async () => {
    if (!result) return;
    setLoading(true);
    try {
      const res = await axios.post(`http://localhost:8000/api/upload/ocr/${result.submittal_id}`);
      setResult(prev => ({ ...prev, text_len: res.data.text_len, quick_flags: res.data.quick_flags }));
    } catch (e) {
      console.error(e);
      alert("OCR failed. Check backend logs and Tesseract installation.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: 16 }}>
      <div style={{ marginBottom: 8 }}>
        <input type="file" accept="application/pdf" onChange={onFileChange} />
        <button onClick={upload} disabled={loading || !file} style={{ marginLeft: 8 }}>
          {loading ? "Uploading..." : "Upload Submittal"}
        </button>
      </div>

      {result && (
        <div style={{ marginTop: 12, border: "1px solid #e5e7eb", padding: 12, borderRadius: 6 }}>
          <h3 style={{ margin: 0 }}>Upload Result</h3>
          <div style={{ marginTop: 8 }}><b>Submittal ID:</b> {result.submittal_id}</div>
          <div><b>Filename:</b> {result.filename}</div>
          <div><b>Text length:</b> {result.text_len}</div>
          <div><b>Needs OCR:</b> {result.needs_ocr ? "Yes" : "No"}</div>

          <div style={{ marginTop: 8 }}>
            <b>Quick Flags:</b>
            <ul>
              {result.quick_flags && result.quick_flags.map((f, i) => (
                <li key={i}>
                  <b>{f.field}</b>: {f.issue} {f.evidence ? <em>— "{f.evidence}"</em> : null}
                </li>
              ))}
            </ul>
          </div>

          {result.needs_ocr && (
            <div style={{ marginTop: 8 }}>
              <button onClick={runOcr} disabled={loading}>
                {loading ? "Running OCR..." : "Run OCR Now"}
              </button>
            </div>
          )}

          <div style={{ marginTop: 8 }}>
            <b>Preview:</b>
            <pre style={{ whiteSpace: "pre-wrap", background: "#f6f6f6", padding: 8 }}>{result.preview}</pre>
          </div>
        </div>
      )}
    </div>
  );
}
