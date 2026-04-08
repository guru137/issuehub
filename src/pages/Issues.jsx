import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../services/api";
import Navbar from "../components/Navbar";

export default function Issues() {
  const { projectId } = useParams();
  const navigate = useNavigate();

  const [issues, setIssues] = useState([]);

  // create issue state
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  // 🔥 NEW STATES
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [sort, setSort] = useState("");

  // 🔥 FETCH ISSUES WITH FILTERS
  const fetchIssues = () => {
  let url = `/issues/${projectId}`;
  let params = [];

  if (search) params.push(`q=${search}`);
  if (status) params.push(`status=${status}`);
  if (sort) params.push(`sort=${sort}`);

  if (params.length > 0) {
    url += "?" + params.join("&");
  }

  API.get(url).then((res) => setIssues(res.data));
};

  useEffect(() => {
    fetchIssues();
  }, [search, status, sort]); // 🔥 auto update when changed

  // 🔥 CREATE ISSUE
  const createIssue = async () => {
    if (!title || !description) {
      alert("Please fill all fields");
      return;
    }

    await API.post("/issues", {
      title,
      description,
      project_id: parseInt(projectId),
      priority: "medium", // default (you can improve later)
    });

    setTitle("");
    setDescription("");
    fetchIssues();
  };

  return (
    <>
      <Navbar />

      <div style={{ padding: "20px" }}>
        <h2>Issues</h2>

        {/* 🔥 CREATE ISSUE */}
        <div style={{ marginBottom: "20px" }}>
          <input
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            style={{ marginRight: "10px" }}
          />

          <input
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            style={{ marginRight: "10px" }}
          />

          <button onClick={createIssue}>Create Issue</button>
        </div>

        {/* 🔥 SEARCH + FILTER + SORT */}
        <div style={{ marginBottom: "20px" }}>
          <input
            placeholder="Search issues"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ marginRight: "10px" }}
          />

          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            style={{ marginRight: "10px" }}
          >
            <option value="">All Status</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="closed">Closed</option>
          </select>

          <select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
          >
            <option value="">Sort</option>
            <option value="created_at">Newest</option>
            <option value="priority">Priority</option>
            <option value="status">Status</option>
          </select>
        </div>

        {/* 🔥 ISSUE LIST */}
        {issues.map((i) => (
          <div
            key={i.id}
            style={{
              padding: "10px",
              border: "1px solid gray",
              marginBottom: "10px",
              cursor: "pointer",
            }}
            onClick={() => navigate(`/issue/${i.id}`)}
          >
            <strong>{i.title}</strong>
            <div>{i.description}</div>
            <div>Status: {i.status}</div>
            <div>Priority: {i.priority}</div> {/* 🔥 NEW */}
          </div>
        ))}
      </div>
    </>
  );
}