import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div style={styles.navbar}>
      <h3 style={styles.logo} onClick={() => navigate("/projects")}>
        IssueHub
      </h3>

      <div>
        <button onClick={() => navigate("/projects")} style={styles.button}>
          Projects
        </button>

        <button onClick={handleLogout} style={styles.logout}>
          Logout
        </button>
      </div>
    </div>
  );
}

const styles = {
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px 20px",
    background: "#282c34",
    color: "white",
  },
  logo: {
    cursor: "pointer",
  },
  button: {
    marginRight: "10px",
    padding: "5px 10px",
    cursor: "pointer",
  },
  logout: {
    padding: "5px 10px",
    background: "red",
    color: "white",
    border: "none",
    cursor: "pointer",
  },
};