
import Link from 'next/link';
import FAQSection from '@/src/components/FAQSection';

export const metadata = {
  title: 'Block Blast Tips & Tricks 2025',
  description: 'Follow Block Blast tips to score higher. Implement proven and tested strategies.',
  openGraph: {
    title: 'Block Blast Tips & Tricks 2025 - Block Blast Solver',
    description: 'Focus on following strategies shared by experts to win any level.',
    url: 'https://blockblastsolverai.com/tips',
    siteName: 'Block Blast Solver',
    locale: 'en_US',
    type: 'website',
  },
  keywords: [
    'Block Blast tips',
    'Block Blast tricks',
  ],
}


export default function CheatsPage() {


  // const [activeIndex, setActiveIndex] = useState(-1);

  const faqs = [
    {
      question: 'Is Block Blast luck based?',
      answer: "Success or failure due to random placements of shapes may feel like luck, but strategy plays an important role to succeed against all odds."
    },
    {
      question: 'Is there a trick to win Block Blast?',
      answer: "The best trick is to go for clearing rows and columns first to maximize score. Avoid isolated single blocks and to foresee board shapes to plan strategy earlier."
    },
    {
      question: 'What move should I make in Block Blast?',
      answer: "Give preference to combo moves, which clear out more than one line. They give more score than a single line. Prioritize keeping corners clear whenever you get an opportunity, its gets hard to fill them later."
    },
    {
      question: 'How to get the highest score ever on Block Blast?',
      answer: "An exponentially higher score is achieved by clearing multiple rows and columns in one move. Focus on creating space for cascading effects. Plan ahead moves and keep corners clear when possible."
    },

    // Add all FAQ items here
  ];


  return (
    <>

      <div className="min-h-screen bg-gradient-to-b from-[#0F172A] via-[#00bfff6b] to-[#0F172A] text-white py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          {/* Hero Section */}
          <section className="text-center mb-16">
            {/* <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-white to-sky-500">
              Block Blast Hacks & Cheats
            </h1> */}


            <h1 className='text-4xl md:text-5xl  mb-4 font-bold tracking-tight text-white text-center'>
              Block Blast Tips To<span className='text-sky-500'> Beat Any Level</span></h1>

            <p className="text-xl text-gray-300">Follow and practice these proven and tested techniques to win any level smoothly.</p>
          </section>

          {/* Features Grid */}
          <section className="mb-16">
            {/* <div className="grid md:grid-cols-2 gap-8"> */}
            <div className="group bg-opacity-50 p-6 rounded-xl border  border-[#9ac8f6] border-opacity-30  shadow-2xl">
              <h2 className="text-2xl font-bold mb-4 text-sky-500">Key Top Scoring Approach</h2>
              <p className="mb-4">Works for adventure and basic levels. Takes 3 seconds to get the winning steps.</p>

              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-semibold text-blue-300">Bottom Up Approach</h3>
                  <p className="text-gray-300">It means to prioritize solving from the bottom.</p>


                  <ul className="space-y-2">
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>It creates a snowball effect</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>Helps to avoid time wastage due to isolated blocks</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>Boosts score by filling both rows and columns usually</span>
                    </li>

                  </ul>

                </div>
                <div>
                  <h3 className="text-xl font-semibold text-blue-300">Pattern Recognition</h3>
                  <p className="text-gray-300">Memorize these most common and of highly great worth patterns.</p>


                  <ul className="space-y-2">
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>T-Shaped</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>Square-Pattern</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>L-Shaped</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>I-Shaped</span>
                    </li>

                  </ul>

                </div>
              </div>
            </div>







            <div className="!p-6 g-style  rounded-xl  shadow-2xl mt-16">
              <h2 className="text-2xl font-bold mb-4 text-white">Refined Approaches</h2>

              <div className="space-y-4">

                <div>

                  <h3 className="text-xl font-semibold text-blue-300">Snowball Effect</h3>

                  <ul className="space-y-2">
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>Plan moves ahead of time</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>Quickly analyze the shapes and board</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>Place those shapes first which may have chance of getting isolated</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>Perform multi step moves</span>
                    </li>

                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-blue-300">Use Block Blast Solver</h3>

                  <ul className="space-y-2">
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>Provide screenshot to our <Link className='underline' href="/"> solver</Link>, it uses advanced algorithms to achieve results</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>Automatically understands the shapes and board</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>Finds the best possible move, to maximize score in each move</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-[#30e00d] mr-2">✓</span>
                      <span>Keeps future moves in consideration by itself</span>
                    </li>

                  </ul>
                </div>



              </div>
            </div>
            {/* </div> */}
          </section>




          {/* Benefits Table */}
          <section className="mb-16">
            <h2 className="text-3xl font-bold mb-6 text-center">Common Mistakes to Avoid</h2>

            <div className="overflow-x-auto">
              <table className="min-w-full bg-gray-800 bg-opacity-50 rounded-lg overflow-hidden">
                <thead className="bg-[#0F1F33] bg-opacity-70">
                  <tr>
                    <th className="py-3 px-4 text-left">Don’t</th>
                    <th className="py-3 px-4 text-left">Do</th>

                  </tr>
                </thead>
                <tbody className="divide-y ">
                  <tr>
                    <td className="py-3 px-4 text-red-400">Solve the board randomly</td>
                    <td className="py-3 px-4 text-[#30e00d] font-medium">
                      Plan earlier and solve to create cascading effect</td>

                  </tr>
                  <tr className='cust-li-tr'>
                    <td className="py-3 px-4 text-red-400">Start solving from top</td>
                    <td className="py-3 px-4 text-[#30e00d] font-medium">
                      Prioritize solving from bottom</td>
                  </tr>
                  <tr>
                    <td className="py-3 px-4 text-red-400">In critical situation solve by yourself</td>
                    <td className="py-3 px-4 text-[#30e00d] font-medium">
                      In complex situation use our refined approaches</td>
                  </tr>


                </tbody>
              </table>
            </div>
          </section>

          {/* Stats Section */}
          <section className="mb-16 w-full text-center">

            <div className="  p-4 rounded-lg flex items-center justify-center flex-col py-16 relative">


              <div className="gradient-background">
                <div className="gradient-sphere sphere-1"></div>
                <div className="gradient-sphere sphere-2"></div>
                <div className="gradient-sphere sphere-3"></div>
                <div className="glow"></div>
                <div className="grid-overlay"></div>
                <div className="noise-overlay"></div>
                <div className="particles-container" id="particles-container"></div>
              </div>


              <div className='content-container'>
                <h2 className="text-2xl font-bold mb-4 text-white">All Set To Become Block Blast Pundit</h2>
                <p className="text-sm text-white">Use our screenshot solver to win any level in the block blast game.</p>



                <button className="mt-8 btn mx-auto text-slate-900 p-[16px] lg:px-[24px] lg:py-[16px] sm:px-[12px] sm:py-[8px] transition-all duration-300 ease-in-out cursor-pointer rounded-lg">

                  <Link href="/"> <span className="text-18px font-bold leading-24px text-center text-[#0F172A]">Start Solving Puzzle</span></Link>


                </button>


              </div>


            </div>


          </section>




<FAQSection faq={faqs}/>
  

        </div>
      </div>
    </>
  );
}