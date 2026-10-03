import { useState } from "react";
import "./App.css";

function App() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!resume) {
      setError("Please upload your resume.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();

    formData.append("resume", resume);
    formData.append("job_description", jobDescription);

    try {
     const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to analyze resume");
      }

      const data = await response.json();

      setResult(data);
    } catch (error) {
      setError(
        "Could not connect to the backend. Make sure FastAPI is running."
      );
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>BERT Resume Matcher</h1>
        <p>
          Compare your resume with a job description using NLP and BERT.
        </p>
      </header>

      <main className="container">
        <section className="card">
          <h2>Analyze Your Resume</h2>

          <label>Upload Resume</label>

          <div className="upload-box">
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setResume(e.target.files[0])}
            />

            {resume && (
              <p className="file-name">
                Selected: {resume.name}
              </p>
            )}
          </div>

          <label>Job Description</label>

          <textarea
            placeholder="Paste the job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />

          <button
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>

          {error && <p className="error">{error}</p>}
        </section>

        {result && (
          <section className="results">
            <div className="score-card">
              <h2>Match Score</h2>

              <div className="score">
                {result.match_score}%
              </div>

              <p>
                Semantic similarity between your resume and the job
                description.
              </p>
            </div>

            <div className="skills-container">
              <div className="skill-card">
                <h2>Matching Skills</h2>

                {result.matching_skills.length > 0 ? (
                  <ul>
                    {result.matching_skills.map((skill) => (
                      <li key={skill}>✓ {skill}</li>
                    ))}
                  </ul>
                ) : (
                  <p>No matching skills found.</p>
                )}
              </div>

              <div className="skill-card">
                <h2>Missing Skills</h2>

                {result.missing_skills.length > 0 ? (
                  <ul>
                    {result.missing_skills.map((skill) => (
                      <li key={skill}>✗ {skill}</li>
                    ))}
                  </ul>
                ) : (
                  <p>No missing skills found.</p>
                )}
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;