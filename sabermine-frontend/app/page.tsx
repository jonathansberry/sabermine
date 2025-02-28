"use client"

import Image from "next/image";
import { useState, useEffect, useCallback, Component } from "react";
import { LinkCreator } from "@components/linkCreator";
import { LinkTable } from "@components/linkTable";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "";

export default function Home() {
    const [text, setText] = useState("");
    const [links, setLinks] = useState([]);

    const fetchLinks = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/all`);
        const data = await response.json();
        setLinks(data.short_urls);
      } catch (error) {
        console.error("Error fetching links:", error);
      }
    };

    useEffect(() => {
      fetchLinks();
    }, []);

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
      const uploadPromises = acceptedFiles.map(async (file) => {
        const formData = new FormData();
        formData.append("file", file);

        try {
          const response = await fetch(`${API_BASE_URL}/upload`, {
            method: "POST",
            body: formData,
          });
          if (!response.ok) {
            throw new Error("Upload failed");
          }
          const data = await response.json();
          return data;
        } catch (error) {
          console.error("Error uploading file:", error);
          return null;
        }
      });
      const uploadedFiles = await Promise.all(uploadPromises);
      fetchLinks();
    }, []);

    const onCreate = async () => {
      console.log(JSON.stringify({ "url": text }));
      try {
        await fetch(`${API_BASE_URL}/shorten_url`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ "url": text }),
        });
        fetchLinks();
      } catch (error) {
        console.error("Error creating entry:", error);
      }
    };

    return (
      <div className="flex flex-col items-center p-6 w-full max-w-2xl mx-auto bg-white shadow-lg rounded-xl md:p-10">
        <div className="flex flex-col items-center mb-6">
          <img src="/logo.png" alt="Sabermine Logo" className="w-16 h-16 md:w-20 md:h-20" />
          <h1 className="text-xl md:text-2xl font-bold mt-2 text-black">URL Shortener & File Uploader</h1>
        </div>

        <LinkCreator text={text} setText={setText} onDrop={onDrop} onCreate={onCreate} />
        <LinkTable links={links} />
      </div>
    );
}
