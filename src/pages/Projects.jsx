import { useEffect, useState } from "react";
import API from "../services/api";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const navigate = useNavigate();

  const fetchProjects = () => {
    API.get("/projects").then((res) => setProjects(res.data));
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  // 🔥 CREATE PROJECT
  const createProject = async () => {
    if (!name || !description) {
      alert("Please fill all fields");
      return;
    }

    if (!name || name.length < 3) {
      alert("Name must be at least 3 characters");
      return;
    }

    if (!description || description.length < 6) {
      alert("Description must be at least 6 characters");
      return;
    }

    await API.post("/projects", {
      name,
      description,
    });

    setName("");
    setDescription("");
    fetchProjects(); // refresh list
  };

  return (
    <>
      <Navbar />

      <div style={{ padding: "20px" }}>
        <h2>Projects</h2>

        {/* 🔥 Create Project Form */}
        <div style={{ marginBottom: "20px" }}>
          <input
            placeholder="Project Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            style={{ marginRight: "10px" }}
          />

          <input
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            style={{ marginRight: "10px" }}
          />

          <button onClick={createProject}>Create</button>
        </div>

        {/* 🔥 Project List */}
        {projects.map((p) => (
          <div
            key={p.id}
            style={{
              padding: "10px",
              border: "1px solid gray",
              marginBottom: "10px",
              cursor: "pointer",
            }}
            onClick={() => navigate(`/issues/${p.id}`)}
          >
            <strong>{p.name}</strong>
            <div>{p.description}</div>
          </div>
        ))}
      </div>
    </>
  );
}