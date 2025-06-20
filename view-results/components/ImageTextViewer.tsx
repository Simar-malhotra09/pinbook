'use client';

import { useEffect, useState } from "react";

export default function ImageTextViewer({ id }: { id: string }) {
  const [text, setText] = useState("");
  const [ground_truth_text, setGround_truth_text]= useState("");
  useEffect(() => {
    fetch(`/yolo-data/${id}.txt`)
      .then((res) => res.text())
      .then(setText)
      .catch(() => setText("Could not load text"));
  }, [id]);
  useEffect(() => {
    fetch(`/yolo-data/ground-truths/${id.replace(/^yolo_/, '')}.txt`)
      .then((res) => res.text())
      .then(setGround_truth_text)
      .catch(() => setGround_truth_text("Could not load text"));
  }, [id]);

  return (
    <div className="w-full">
      {/* Labels */}
      <div className="flex w-full font-semibold text-center border-b pb-2">
        <div className="w-1/3 border-r">Image</div>
        <div className="w-1/3 border-r">Prediction</div>
        <div className="w-1/3">Ground Truth</div>
      </div>

      {/* Content */}
      <div className="flex w-full">
        <img
          src={`/yolo-data/${id}.jpg`}
          alt={`YOLO image ${id}`}
          className="w-1/3 object-contain border-r"
        />
        <pre className="w-1/3 text-center p-4 whitespace-pre-wrap text-lg border-r">
          {text.split(" ").join(", ")}
        </pre>
        <pre className="w-1/3 text-center p-4 whitespace-pre-wrap text-lg">
          {ground_truth_text.split(" ").join(", ")}
        </pre>
      </div>
    </div>
  );
}
