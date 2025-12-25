'use client';

import { useState } from "react";


type Props = {
  question: string;
  children: React.ReactNode;
};

export default function FAQAccordion({ question, children }: Props) {
  const [activeIndex, setActiveIndex] = useState(false);

  return (
          <div
            className="border border-white/10 rounded-xl p-4 cursor-pointer my-4  post-faq"
            onClick={() =>
              setActiveIndex(!activeIndex)
            }
          >
            <div className="flex justify-between items-center">
              <h3 className="font-semibold">{question}</h3>
              <span>{activeIndex  ? "−" : "+"}</span>
            </div>

            {activeIndex && (
              <p className="mt-4 text-gray-300">
                {children}
              </p>
            )}
          </div>
  );
}
