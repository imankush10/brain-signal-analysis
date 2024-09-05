import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Homepage from "./components/Homepage";
import FileUpload from "./components/FileUpload";
import Dashboard from "./components/Dashboard";

// create routes
const router = createBrowserRouter([
  {
    path: "/",
    element: <Homepage />,
  },
  {
    path: "/upload",
    element: <FileUpload />,
  },
  {
    path: "/dashboard",
    element: <Dashboard />,
  },
]);

function App() {
  return (
    <div className="bg-[#f1f2f6] text-black"
    >
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
