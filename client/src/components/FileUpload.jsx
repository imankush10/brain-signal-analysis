import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import { useNavigate } from "react-router-dom";
import NavBar from "./NavBar";

function FileUpload() {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const onDrop = (acceptedFiles) => {
    setFile(acceptedFiles[0]);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      if (
        data.attention_score !== undefined &&
        data.mean_squared_error !== undefined
      ) {
        navigate('/dashboard', { state: { ...data, file } });
      } else {
        console.error(data.error);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <>
      <NavBar />
      <div className="flex h-80 flex-col justify-center items-center bg-white">
        <div
          {...getRootProps()}
          className="flex flex-col items-center justify-center h-52 w-full max-w-md p-6 border-2 border-dashed border-gray-300 bg-gray-100 text-gray-600 cursor-pointer"
        >
          <input {...getInputProps()} />
          {isDragActive ? (
            <p>Drop the files here</p>
          ) : (
            <p>Drag & drop some files here, or click to select files</p>
          )}
        </div>
        <button
          onClick={handleUpload}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Upload
        </button>
      </div>
    </>
  );
}

export default FileUpload;
