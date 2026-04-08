import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import API from "../services/api";
import Navbar from "../components/Navbar";

export default function IssueDetail() {
  const { id } = useParams();

  const [issue, setIssue] = useState(null);
  const [comments, setComments] = useState([]);
  const [text, setText] = useState("");
  const [status, setStatus] = useState("");

  // 🔥 Fetch issue + comments
  const fetchData = async () => {
    const issueRes = await API.get(`/issues/${id}`); // if not available, skip
    setIssue(issueRes.data);

    const commentRes = await API.get(`/comments/${id}`);
    setComments(commentRes.data);
  };

  useEffect(() => {
    fetchData();
  }, []);

  // 🔥 Add comment
  const addComment = async () => {
    if (!text) return;

    await API.post(`/comments/${id}`, { body: text });
    setText("");
    fetchData();
  };

  // 🔥 Update status
  const updateStatus = async () => {
    await API.put(`/issues/status/${id}?status=${status}`);
    fetchData();
  };

  // 🔥 Assign user
  const assignUser = async () => {
    const userId = prompt("Enter user ID");
    if (!userId) return;

    await API.put(`/issues/assign/${id}/${userId}`);
    fetchData();
  };

  if (!issue) return <div>Loading...</div>;

  return (
    <>
      <Navbar />

      <div style={{ padding: "20px" }}>
        <h2>{issue.title}</h2>
        <p>{issue.description}</p>
        <p>Status: {issue.status}</p>

        {/* 🔥 Status Update */}
        <div>
          <select onChange={(e) => setStatus(e.target.value)}>
            <option value="">Change Status</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="closed">Closed</option>
          </select>
          <button onClick={updateStatus}>Update</button>
        </div>

        {/* 🔥 Assign User */}
        <button onClick={assignUser}>Assign User</button>

        <hr />

        {/* 🔥 Comments */}
        <h3>Comments</h3>

        {comments.map((c) => (
          <div key={c.id} style={{ marginBottom: "10px" }}>
            {c.body}
          </div>
        ))}

        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Add comment"
        />
        <button onClick={addComment}>Add</button>
      </div>
    </>
  );
}