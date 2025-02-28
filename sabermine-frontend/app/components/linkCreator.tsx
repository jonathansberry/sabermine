import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Button } from "@components/button";
import { LinkCreatorProps } from "@types";


export function LinkCreator({ text, setText, onDrop, onCreate }: LinkCreatorProps) {
    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

    return (
      <div
        {...getRootProps()}
        className="w-full border-2 border-dashed border-black p-6 md:p-10 rounded-lg cursor-pointer bg-white hover:bg-gray-100 transition flex flex-col items-center text-center"
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p className="text-black font-medium">Drop the files here...</p>
        ) : (
          <p className="text-black font-medium">Drag & drop files to upload here, or enter a custom url to shorten. </p>
        )}

        <div className="flex flex-col md:flex-row items-center mt-4 w-full max-w-md bg-white p-2 rounded-lg border border-black">
          <input
            type="text"
            placeholder="https://example-long-url.io"
            className="flex-1 p-2 border text-black border-black rounded-lg focus:outline-none"
            value={text}
            onChange={(e) => setText(e.target.value)}
            onClick={(event) => event.stopPropagation()}
          />
          <Button
            className="mt-2 md:mt-0 md:ml-2 bg-black text-white px-4 py-2 rounded-lg w-full md:w-auto"
            onClick={(event) => {
              event.stopPropagation();
              onCreate();
            }}
          >
            Shorten!
          </Button>
        </div>
      </div>
    );
  }
