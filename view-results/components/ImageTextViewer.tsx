'use client';

import { useEffect, useState } from "react";

export default function ImageTextViewer({ id }: { id: string }) {
  const [text, setText] = useState("");

  useEffect(() => {
    fetch(`/yolo-data/${id}.txt`)
      .then((res) => res.text())
      .then(setText)
      .catch(() => setText("Could not load text"));
  }, [id]);

  return (
    <div className="flex w-full">
      <img
        src={`/yolo-data/${id}.jpg`}
        alt={`YOLO image ${id}`}
        className="w-1/2 object-contain border-r"
      />
      <pre className="w-1/2 text-center p-4 whitespace-pre-wrap text-lg">{text}</pre>
    </div>
  );
}
