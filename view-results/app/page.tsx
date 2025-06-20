'use client';

import { useEffect, useState } from "react";
import ImageTextViewer from "@/components/ImageTextViewer";

export default function Home() {
  const [entries, setEntries] = useState<string[]>([]);
  const [page, setPage] = useState(0);

  const ITEMS_PER_PAGE = 1;

  useEffect(() => {
    fetch("/yolo_data_index.json")
      .then(res => res.json())
      .then(setEntries)
      .catch(() => setEntries([]));
  }, []);

  const current = entries.slice(page * ITEMS_PER_PAGE, (page + 1) * ITEMS_PER_PAGE);

  const next = () => setPage((p) => Math.min(p + 1, entries.length - 1));
  const prev = () => setPage((p) => Math.max(p - 1, 0));

  if (entries.length === 0) return <p>Loading...</p>;

  return (
    <div className="flex flex-col items-center p-50">
        <div className="flex w-full max-w-10xl border">
          <ImageTextViewer id={current[0]} />
        </div>
        <div className="mt-4 flex gap-4 items-center">
          <button onClick={prev} disabled={page === 0}>Previous</button>
          <span>Page {page + 1} / {entries.length}</span>
          <button onClick={next} disabled={page >= entries.length - 1}>Next</button>
        </div>
    </div>
  );
}
