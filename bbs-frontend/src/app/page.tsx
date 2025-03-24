'use client'

import { FC, useState } from 'react'
import { Button, buttonVariants } from '@/ui/button'
import { FileInput } from '@/ui/file-input'
import example from "public/example.png"
import manualIcon from "public/manual-icon.png"
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import Image from 'next/image'
import tinycolor from 'tinycolor2'


export const metadata = {
  title: 'ImageToAlt - Home',
}

const Page: FC = () => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  // Function to clear the uploaded file
  const clearFile = () => {
    setUploadedFile(null);
    setHideComp((prev) => !prev);
    console.log(hideComp);
    console.log(uploadedFile);
  }

  interface Step {
    board: number[][];
    completedLines: number;
  }

  const [hideComp, setHideComp] = useState(false);
  const [steps, setSteps] = useState<Step[]>([]);
  const [shapeColors, setShapeColors] = useState<Record<string, string>>({});

  // This will receive the steps from FileInput
  const handleUploadSuccess = (
    receivedSteps: Step[],
    receivedShapeColors: Record<string, string>
  ) => {
    setSteps(receivedSteps);
    setShapeColors(receivedShapeColors);
    setHideComp((prev) => !prev);
  };




  function getDynamicStyles(baseColor: string) {
    // Calculate gradient colors
    const lighter = tinycolor(baseColor).lighten(20).toString();
    const darker = tinycolor(baseColor).darken(20).toString();
    const backgroundGradient = `linear-gradient(to bottom right, ${lighter}, ${darker})`;

    // Compute box shadow colors based on base color modifications
    const innerShadow1 = tinycolor(baseColor).saturate(20).setAlpha(0.8).toRgbString();
    const innerShadow2 = tinycolor(baseColor).darken(30).toRgbString();
    const innerShadow3 = tinycolor(baseColor).lighten(40).setAlpha(0.5).toRgbString();

    // Compute border color (a darker variant)
    const borderColor = tinycolor(baseColor).darken(30).toString();

    return {
      background: backgroundGradient,
      boxShadow: `inset 4px 4px 6px ${innerShadow1}, inset -4px -4px 6px ${innerShadow2}, inset 2px 2px 4px ${innerShadow3}, 2px 2px 4px rgba(0, 0, 0, 0.5)`,
      border: `1px solid ${borderColor}`,
    };
  }




  return (



    <main className='relative bg-white'>

      <section className="w-full grid items-center lg:gap-20 gap-6 pt-6 pb-0 md:pt-10 bg-[#0F172D]">
        <div className="container flex w-full  flex-col items-start gap-2  bg-red-600">
          <h1 className="text-3xl font-extrabold leading-tight tracking-tighter sm:text-3xl md:text-5xl lg:text-6xl">
            Block Blast Solver
          </h1>

        </div>







        {/* Try Another Button */}
        {uploadedFile && (
          <Tooltip>
            <TooltipTrigger asChild>
              <div className="flex justify-center w-full my-4">
                <Button
                  disabled={!uploadedFile}
                  className={buttonVariants({
                    size: "lg",
                    className: "w-fit hover:!bg-[#468beb] hover:!text-white"
                  })}
                  onClick={clearFile}
                >
                  Try Another


                  <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-rotate-cw ml-1"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8" /><path d="M21 3v5h-5" /></svg>


                </Button>
              </div>
            </TooltipTrigger>
            <TooltipContent className="!bg-[#316edf] !text-white">
              <p>Get results for next move</p>
            </TooltipContent>
          </Tooltip>
        )}




        {/* Upload Section */}



        <div className={`${hideComp ? "hidden" : "flex"} flex-col lg:flex-row md:flex-row gap-4 lg:gap-20 justify-center items-stretch bg-[#274aa6] py-8 px-2 lg:p-10 rounded-lg z-10 container`}>
          {/* Pass uploadedFile state and setter to FileInput */}
          <FileInput uploadedFile={uploadedFile} setUploadedFile={setUploadedFile} onUploadSuccess={handleUploadSuccess} />

          <div className="flex flex-col justify-center items-center gap-4 w-full lg:w-1/2 md:w-1/2 bg-[#0f172d] rounded-lg py-8 px-2 lg:p-10 border-4 border-[#9ac8f6] border-solid">

            <Image
              className="rounded-lg"
              src={example}
              alt="Uploaded Preview"
              width={150}
              height={150}
              loading="lazy"
            />


            <span>OR</span>

            <button className="flex items-center justify-center gap-3 bg-[#468beb] text-white p-[16px] lg:px-[24px] lg:py-[16px] rounded-lg hover:bg-[#316edf] w-[200px] lg:w-[252px] h-[56px]">
              <Image alt="select image" className="w-[32px] h-[32px] aspect-square" src={manualIcon} />
              <span className="text-18px font-semibold leading-24px text-center">Fill Manually</span>
            </button>
          </div>
        </div>




        {uploadedFile && (
          <div className="steps-container-wrapper">
            {steps.map((step, stepIndex) => {
              // Compute completed rows and columns from the board in this step.
              const completedRows = step.board.map((row) => row.every((cell) => cell !== 0));
              const completedColumns = step.board[0].map((_, colIndex) =>
                step.board.every((row) => row[colIndex] !== 0)
              );

              return (
                <div key={stepIndex} className="step-container">
                  <p>Step {stepIndex + 1}</p>
                  <p>Completed Lines: {step.completedLines}</p>
                  <div className="board">
                    {step.board.map((row, rowIndex) => (
                      <div key={rowIndex} className="row">
                        {row.map((cell, cellIndex) => {
                          // Determine the base class for each cell.
                          const cellClass =
                            cell === 0 ? 'empty' : cell === 1 ? 'block' : 'placed';

                          // Default style.
                          let style = {};

                          // Mapping: 2 -> shape 0, 3 -> shape 1, 4 -> shape 2.
                          if (cell === 2) {
                            style = shapeColors?.["shape 0"]
                              ? getDynamicStyles(shapeColors["shape 0"])
                              : { backgroundColor: shapeColors?.["shape 0"] };
                          } else if (cell === 3) {
                            style = shapeColors?.["shape 1"]
                              ? getDynamicStyles(shapeColors["shape 1"])
                              : { backgroundColor: shapeColors?.["shape 1"] };
                          } else if (cell === 4) {
                            style = shapeColors?.["shape 2"]
                              ? getDynamicStyles(shapeColors["shape 2"])
                              : { backgroundColor: shapeColors?.["shape 2"] };
                          }

                          // If the row or the column is complete, add a white border.
                          if (completedRows[rowIndex] || completedColumns[cellIndex]) {
                            style = { ...style, border: "2px solid #4dff00" };
                          }

                          return (
                            <div
                              key={cellIndex}
                              className={`cell ${cellClass}`}
                              style={style}
                            >
                              {/* Optionally render cell content */}
                            </div>
                          );
                        })}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}





        {uploadedFile && (


          <div className="flex flex-col justify-center items-center">
            <p className='text-white text-lg font-bold my-5'>Uploaded Screenshot</p>

            <Image
              src={URL.createObjectURL(uploadedFile)}
              alt="Uploaded Preview"
              width={200}
              height={100}
              className="object-cover rounded-lg mx-auto mb-2 lg:w-1/6 lg:h-[auto] md:w-1/4 sm:w-full md:h-[auto]"
            />
          </div>

        )}



        <div className="absolute top-[700px] left-0 w-full z-0">
          <svg className='w-full h-[600]px' xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#fff" fill-opacity="1" d="M0,256L1440,64L1440,0L0,0Z"></path></svg>
        </div>



        <div className='bg-white pt-10 z-10'>
          <div className="container flex w-full flex-col items-start gap-2 ">




            <p className="text-lg text-slate-700 dark:text-slate-400 sm:text-xl">
              <strong>It&apos;s an AI-based problem solver</strong> that finds the best possible moves for a Block Blast game using just a screenshot of your gameplay. You can achieve a high score in the game with a single click using our free online tool.
            </p>
            <p className="text-lg text-slate-700 dark:text-slate-400 sm:text-xl">
              What makes it better than other helpers is its advanced solver algorithms. Block Blast Solver finds the best possible steps to take to maximize your score in a given situation.
            </p>
            <p className="text-lg text-slate-700 dark:text-slate-400 sm:text-xl">
              Also, its solution helps you understand the right place for the right shape with the help of 3D design and colors. Unlike others, this online solver represents each shape with its original color for a better understanding of the player, which makes it the best.
            </p>
          </div>
        </div>

      </section>

      <section>
        <h2>How to Use Block Blast Solver?</h2>
        <p>You only need to upload 1 picture for each step, however, be sure to follow these steps to get accurate results. Otherwise, the Block Blast AI solver will not be able to help you with cheat moves.</p>
      </section>

      <section>
        <h3>Step 1: Set up the game</h3>
        <p>If your mobile screen frame is according to the following list, you are good to go for the next step, which is taking a screenshot.</p>

        <ol>
          <li>The game board should be clearly visible.</li>
          <li>There should be a complete screenshot in raw form, any cropped or edited picture will result in false outputs.</li>
          <li>All the given shapes should be visible.</li>
          <li>At least one out of the three given shapes must be visible for the Block Blast Solver to work properly.</li>
          <li>There should be no ad popup, loading screen, or game animation.</li>
        </ol>
      </section>

      <section>

        <h3>Step 2: Take the Screenshot</h3>
        <details>
          <summary><h4>For Android:</h4></summary>
          <table>
            <thead>
              <tr>
                <th>Method</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Using Buttons</strong></td>
                <td>Press and hold the Power button + Volume Down button. You&apos;ll see a flash on the screen, and a screenshot will appear for preview. It will be saved in the Gallery or Photos app under the &quot;Screenshots&quot; folder.</td>
              </tr>
              <tr>
                <td><strong>Using Gestures (Some Android Phones)</strong></td>
                <td>On Samsung, OnePlus, Xiaomi, and other brands, you can swipe three fingers down or palm swipe to take a screenshot. You can enable it by going to Settings &gt; Advanced Features &gt; Motions and Gestures and enabling the option.</td>
              </tr>
              <tr>
                <td><strong>Using Google Assistant or Bixby:</strong></td>
                <td>Say &quot;Hey Google, take a screenshot&quot; or &quot;Hey Bixby, take a screenshot&quot;.</td>
              </tr>
              <tr>
                <td><strong>Using Quick Settings</strong></td>
                <td>Swipe down the Quick Settings menu. Look for the Screenshot option and tap it.</td>
              </tr>
            </tbody>
          </table>
        </details>

        <details>
          <summary><h4>For iPhone:</h4></summary>
          <table>
            <thead>
              <tr>
                <th>Method</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Using Buttons</strong></td>
                <td>For iPhones with Face ID (No Home Button - iPhone X and later): Press and hold the Side Button + Volume Up button together.
                  For iPhones with a Home Button (iPhone 8, SE, and earlier): Press and hold the Home Button + Power Button together.
                  The screen will flash, and a preview will appear in the bottom-left corner.
                  Saved screenshots will appear in the Photos app &gt; Screenshots folder.</td>
              </tr>
              <tr>
                <td><strong>Using AssistiveTouch (No Buttons Needed)</strong></td>
                <td> Go to Settings &gt; Accessibility &gt; Touch &gt; AssistiveTouch and turn it on.
                  Tap the AssistiveTouch button &gt; Device &gt; More &gt; Screenshot.
                </td>
              </tr>
              <tr>
                <td><strong>Using Back Tap (iOS 14 and later)</strong></td>
                <td> Go to Settings &gt; Accessibility &gt; Touch &gt; Back Tap.
                  Set Double Tap or Triple Tap to Screenshot.
                  Now, double-tap or triple-tap the back of your iPhone to take a screenshot.
                </td>
              </tr>
            </tbody>
          </table>
        </details>
      </section>

      <section>
        <h3>Common Mistakes to Avoid</h3>
        <h4>What to Do</h4>
        <ul>
          <li>Upload raw screenshots.</li>
          <li>Set phone brightness to the maximum level.</li>
          <li>Take a clean full-screen screenshot by waiting for the game and text animations to complete.</li>
        </ul>

        <h4>What to Avoid</h4>
        <ul>
          <li>Crop or edit the screenshot.</li>
          <li>Keep phone brightness too low.</li>
          <li>The screenshot includes any overlays or effects of ad pop-ups, and game/loading animations visible.</li>
        </ul>
      </section>



      <section>

        <h3>Screenshot Examples</h3>
        <h4>Valid Captures</h4>
        <h4>Invalid Captures</h4>


      </section>



      <section>

        <h3>Upload Or Draw: </h3>
        <p>Click the upload button and select a screenshot from your device, or you can manually draw your shapes and board. Once the upload is completed, then an algorithm that is specifically designed for this game will find solutions automatically, just wait a few seconds for a response.</p>

        <h3>Solve and play:</h3>

        <p>The final output of the combo solver will contain all 3 steps with solutions. Each shape will be placed in a position that maximizes your score or sets up the next move for a high-scoring play. Completed rows or columns will be highlighted using a green border. Each shape in the output will retain the same color and form as it has in the uploaded screenshot.</p>



      </section>



      <section>


        <h2>Frequently Asked Questions</h2>

        <p>Discover tips, tricks and hacks for the Block Blast game. Whether you&apos;re a newbie or a pro player, quickly get clear information with our frequently asked question&apos;s answers.</p>



        <h2>How does the Block Blast game work?</h2>


        <p>It&apos;s a puzzle game that challenges the player&apos;s ability to find suitable positions on the grid for given shapes. A grid has an 8x8 structure consisting of 8 rows and 8 columns, while shapes can be simple or complex, e.g., L, T, square, rectangle shapes. As the game continues, the difficulty increases with more difficult puzzle levels and complex shapes. If by placing the shape on a grid any row or column gets completed, the user earns a score for that.</p>

        <h2>How to get a really high score in Block Blast?</h2>

        <p>Achieving a high score requires implementing effective strategies. Try to create chain reactions that open up opportunities for future moves. Consistently planning your shape placements in advance can trigger cascading effects, helping you maintain high scores. Remember, your high score is based on clearing the maximum number of rows or columns using the given shapes.</p>

        <h2>What is a Block Blast Solver?</h2>
        <p>It&apos;s a free online tool that provides unlimited help to decide on shape placement order after pattern recognition of blocks on the grid for the players. It requires simply a single image from the current gameplay of the player. There are no restrictions on the attempts, so upload as many images as you want for assistance, but one for each streak.</p>

        <h2>How to get a Block Blast Solver?</h2>
        <p>If you prefer using a laptop or computer for picture solver you can find our website-based tool using any search engine like Google. Or you can download free and install our app from the Play Store for Android and the App Store for iOS.</p>


      </section>

















      <footer className="flex flex-col gap-4 mt-12">
        <div className="flex items-center gap-4">
          <Button href="/terms" className={buttonVariants({ variant: 'link', size: 'sm' })}>
            Terms
          </Button>
          <Button href="/privacy-policy" className={buttonVariants({ variant: 'link', size: 'sm' })}>
            Privacy Policy
          </Button>
        </div>
      </footer>


    </main>













  )
}

export default Page
