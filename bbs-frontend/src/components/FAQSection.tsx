'use client';

import { useState } from "react";


type FAQItem = {
  question: string;
  answer: string;
};

type Props = {
  faq: FAQItem[];
};

export default function FAQSection({ faq }: Props) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  const toggleAccordion = (index: number) => {
    setActiveIndex(activeIndex === index ? null : index);
  };


  return (
         <section className="py-6" aria-label="FAQ Section">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              <div className="mb-16">
  
  
  
                <h2 className='text-4xl md:text-4xl font-bold tracking-tight text-white text-center'> Frequently Asked<span className='text-sky-500'> Questions</span></h2>
  
             
              </div>
              <div className="accordion-group">
                {faq.map((faq, index) => (
                  <div
                    key={index}
                    className={`accordion border border-solid  border-white/10 p-4 rounded-xl transition duration-500 mb-8 lg:p-4 ${activeIndex === index ? 'active' : ''
                      }`}
                  >
                    <button
                      className="group inline-flex items-center justify-between text-left text-lg font-normal leading-8 w-full transition duration-500 "
                      onClick={() => toggleAccordion(index)}
                      aria-expanded={activeIndex === index}
                    >
                      <h3 className='text-white font-extrabold'>{faq.question}</h3>
                      <div className="flex items-center">
                        <svg
                          className={`w-6 h-6 transition duration-500 ${activeIndex === index ? 'hidden' : 'block'
                            }`}
                          viewBox="0 0 24 24"
                        >
                          <path d="M6 12H18M12 18V6" stroke="currentColor" strokeWidth="1.6" />
                        </svg>
                        <svg
                          className={`w-6 h-6 transition duration-500 ${activeIndex === index ? 'block' : 'hidden'
                            }`}
                          viewBox="0 0 24 24"
                        >
                          <path d="M6 12H18" stroke="currentColor" strokeWidth="1.6" />
                        </svg>
                      </div>
                    </button>
                    <div
                      className={`overflow-hidden transition-all duration-300 ${activeIndex === index ? 'max-h-[500px]' : 'max-h-0'
                        }`}
                    >
                      <p className="text-base text-gray-300 font-normal leading-6 pt-4">
                        {faq.answer}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>
  )

}