import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import NavBar from "./NavBar";
import DashboardData from "./DashboardData";

function Dashboard() {
  const location = useLocation();
  const { attention_score, mean_squared_error } = location.state || {};
  const [visualizations, setVisualizations] = useState([]);

  useEffect(() => {
    const fetchVisualizations = async () => {
      const formData = new FormData();
      formData.append("file", location.state.file);

      try {
        const response = await fetch(
          "http://127.0.0.1:5000/generate_visualizations",
          {
            method: "POST",
            body: formData,
          }
        );

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        setVisualizations(data.visualizations);
      } catch (error) {
        console.error("Error fetching visualizations:", error);
      }
    };

    if (location.state.file) {
      fetchVisualizations();
    }
  }, [location.state.file]);

  return (
    <>
      <DashboardData
        img1={visualizations[0]}
        img2={visualizations[1]}
        score1={attention_score}
        score2={mean_squared_error}
      />
    </>
  );
}

export default Dashboard;
