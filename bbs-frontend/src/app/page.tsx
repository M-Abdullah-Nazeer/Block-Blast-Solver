'use client'

import { FC, useState } from 'react'
import { Button, buttonVariants } from '@/ui/button'
import { FileInput } from '@/ui/file-input'
import example from "public/example.png"
import manualIcon from "public/manual-icon.png"
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import Image from 'next/image'
import tinycolor from 'tinycolor2'
import { motion, useMotionValue } from "framer-motion";
import { useMotionTemplate } from "framer-motion";


import { MouseEvent as ReactMouseEvent } from "react";




// const innerShadow1 = '#0d8abccc';  // Darker blue shadow
// const innerShadow2 = '#e6f4ff99';  // Frosted white highlight
// const innerShadow3 = '#1a73e899';  // Mid-tone blue accent
// const borderColor = '#e6f4ff9';    // Light blue border


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



  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  function handleMouseMove({
    currentTarget,
    clientX,
    clientY,
  }: React.MouseEvent<HTMLDivElement>) {
    const { left, top } = currentTarget.getBoundingClientRect();
    mouseX.set(clientX - left);
    mouseY.set(clientY - top);
  }

  const background = useMotionTemplate`radial-gradient(650px circle at ${mouseX}px ${mouseY}px, rgba(14, 165, 233, 0.15), transparent 80%)`;

  return (



    <main className='relative bg-[#111827] container'>

      <section className="w-full grid items-center lg:gap-20 gap-6 pt-6 pb-0 md:pt-10 bg-[#0F172D]">
        <div className="container flex w-full  flex-col items-start gap-2  bg-red-600">
          <h1 className="text-5xl font-extrabold leading-tight tracking-tighter sm:text-3xl md:text-5xl lg:text-6xl">
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



        {/* <div className="absolute top-[700px] left-0 w-full z-0">
          <svg className='w-full h-[600]px' xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#fff" fill-opacity="1" d="M0,256L1440,64L1440,0L0,0Z"></path></svg>
        </div> */}



        <div className='bg-white pt-10 z-10'>
          <div className="container flex w-full flex-col items-start gap-2 ">




            <p className="text-lg text-[#0F172D] dark:text-[#0F172D] sm:text-xl">
              <strong>It&apos;s an AI-based problem solver</strong> that finds the best possible moves for a Block Blast game using just a screenshot of your gameplay. You can achieve a high score in the game with a single click using our free online tool.
            </p>
            <p className="text-lg text-[#0F172D] dark:text-[#0F172D] sm:text-xl">
              What makes it better than other helpers is its advanced solver algorithms. Block Blast Solver finds the best possible steps to take to maximize your score in a given situation.
            </p>
            <p className="text-lg text-[#0F172D] dark:text-[#0F172D] sm:text-xl">
              Also, its solution helps you understand the right place for the right shape with the help of 3D design and colors. Unlike others, this online solver represents each shape with its original color for a better understanding of the player, which makes it the best.
            </p>
          </div>
        </div>

      </section>



      <section className='my-8'>


        <h2 className='text-4xl text-sky-500 font-bold tracking-tight text-center'>How to Use <strong className='mark'>Block Blast Solver?</strong></h2>
        <p className='mt-6 text-base leading-7 text-gray-300 text-center'>You only need to upload 1 picture for each step, however, be sure to follow these steps to get accurate results. Otherwise, the Block Blast AI solver will not be able to help you with cheat moves.</p>


        <div className=" bg-gray-900 p-0 my-8 md:p-8 grid  grid-cols-1 md:grid-cols-[1fr_2fr] items-center justify-center gap-8 md:gap-[20px] lg:gap-[50px] xl:gap-[100px]">




          <div className="group relative max-w-md rounded-xl border border-white/10 bg-gray-900 lg:px-8 md:px-6 p-4 md:py-8 lg:py-16 shadow-2xl"
            onMouseMove={handleMouseMove}
          >
            <motion.div
              className="pointer-events-none absolute -inset-px rounded-xl opacity-0 transition duration-300 group-hover:opacity-100"
              style={{ background }}
            />
            <div>

              <div className="mt-2 flex items-center gap-x-2">


                <h3 className="text-2xl md:text-3xl font-bold tracking-tight text-white h3-cust">

                  <span className="text-base font-semibold leading-7 text-sky-500 mb-2">
                    Step 1:
                  </span>
                  Set up the game
                </h3>
              </div>
              <p className="mt-6 text-base leading-7 text-gray-300">
                If your mobile screen frame is according to the following list, you are good to go for the next step, which is taking a screenshot.
              </p>
            </div>
          </div>



          <div className="flex flex-col">


            <ul className='cust-li'>

              <li>The game board should be clearly visible.</li>
              <li>There should be a complete screenshot in raw form, any cropped or edited picture will result in false outputs.</li>
              <li>All the given shapes should be visible.</li>
              <li>At least one out of the three given shapes must be visible for the Block Blast Solver to work properly.</li>
              <li>There should be no ad popup, loading screen, or game animation.</li>

            </ul>

          </div>





        </div>

      </section>

      <section className='step2'>



        <h3 className='text-2xl md:text-3xl font-bold tracking-tight text-white text-center h3-cust'>
          <span className="text-base font-semibold leading-7 text-sky-500 text-center mb-2">
            Step 2:
          </span>
          Take the Screenshot</h3>


        <div className="bg-gray-900 p-0 md:p-8 grid  grid-cols-1 lg:grid-cols-[1fr_1fr] items-start justify-center gap-8">

          <details className="group relative rounded-xl border border-white/10 bg-gray-900 lg:px-8 md:px-6 p-0 md:py-8 lg:py-16 shadow-2xl"
          >



            <summary><h4>For Android</h4>

              <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="40" height="40" viewBox="0,0,256,256"
                fill="#FFFFFF;">
                <g fill="#ffffff" fill-rule="nonzero" stroke="none" stroke-width="1" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none" text-anchor="none"><g transform="scale(4,4)"><path d="M19.92578,4.45898c-0.12891,0.01597 -0.2555,0.05795 -0.375,0.12695c-0.478,0.276 -0.64319,0.88723 -0.36719,1.36523l2.68945,4.6582c-3.45074,2.73959 -5.89874,6.80214 -6.62695,11.39063h33.57422c-0.63375,-4.69499 -3.0921,-8.7927 -6.62109,-11.51367l2.61719,-4.53516c0.276,-0.478 0.11081,-1.08923 -0.36719,-1.36523c-0.478,-0.276 -1.08924,-0.11277 -1.36523,0.36523l-2.55078,4.41797c-2.42063,-1.44629 -5.21465,-2.30781 -8.20898,-2.36523c-3.21465,-0.06145 -6.23025,0.84124 -8.81445,2.43945l-2.59375,-4.49219c-0.207,-0.3585 -0.60352,-0.54009 -0.99023,-0.49219zM24.5,14c0.828,0 1.5,0.672 1.5,1.5c0,0.828 -0.672,1.5 -1.5,1.5c-0.828,0 -1.5,-0.672 -1.5,-1.5c0,-0.828 0.672,-1.5 1.5,-1.5zM39.5,14c0.828,0 1.5,0.672 1.5,1.5c0,0.828 -0.672,1.5 -1.5,1.5c-0.828,0 -1.5,-0.672 -1.5,-1.5c0,-0.828 0.672,-1.5 1.5,-1.5zM15.03906,24.05469c-0.012,0.266 -0.03906,0.52887 -0.03906,0.79687v21.05469c0,2.26 1.791,4.09375 4,4.09375h3v6.5c0,1.381 1.119,2.5 2.5,2.5c1.381,0 2.5,-1.119 2.5,-2.5v-6.5h10v6.5c0,1.381 1.119,2.5 2.5,2.5c1.381,0 2.5,-1.119 2.5,-2.5v-6.5h3c2.209,0 4,-1.83375 4,-4.09375v-20.95898zM9.5,25c-1.381,0 -2.5,1.119 -2.5,2.5v8c0,1.381 1.119,2.5 2.5,2.5c1.381,0 2.5,-1.119 2.5,-2.5v-8c0,-1.381 -1.119,-2.5 -2.5,-2.5zM54.5,25c-1.381,0 -2.5,1.119 -2.5,2.5v8c0,1.381 1.119,2.5 2.5,2.5c1.381,0 2.5,-1.119 2.5,-2.5v-8c0,-1.381 -1.119,-2.5 -2.5,-2.5z"></path></g></g>
              </svg>

            </summary>
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

          <details className="group relative rounded-xl border border-white/10 bg-gray-900 lg:px-8 md:px-6 p-0 md:py-8 lg:py-16 shadow-2xl">
            <summary><h4>For iPhone</h4>
              <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="40" height="40" viewBox="0 0 48 48">
                <path fill="white" d="M 44.527344 34.75 C 43.449219 37.144531 42.929688 38.214844 41.542969 40.328125 C 39.601563 43.28125 36.863281 46.96875 33.480469 46.992188 C 30.46875 47.019531 29.691406 45.027344 25.601563 45.0625 C 21.515625 45.082031 20.664063 47.03125 17.648438 47 C 14.261719 46.96875 11.671875 43.648438 9.730469 40.699219 C 4.300781 32.429688 3.726563 22.734375 7.082031 17.578125 C 9.457031 13.921875 13.210938 11.773438 16.738281 11.773438 C 20.332031 11.773438 22.589844 13.746094 25.558594 13.746094 C 28.441406 13.746094 30.195313 11.769531 34.351563 11.769531 C 37.492188 11.769531 40.8125 13.480469 43.1875 16.433594 C 35.421875 20.691406 36.683594 31.78125 44.527344 34.75 Z M 31.195313 8.46875 C 32.707031 6.527344 33.855469 3.789063 33.4375 1 C 30.972656 1.167969 28.089844 2.742188 26.40625 4.78125 C 24.878906 6.640625 23.613281 9.398438 24.105469 12.066406 C 26.796875 12.152344 29.582031 10.546875 31.195313 8.46875 Z"></path>
              </svg>
            </summary>
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

        </div>



      </section>

      <section>

        <h3 className='text-2xl md:text-3xl font-bold tracking-tight text-white text-center h3-cust'>
          <span className="text-base font-semibold leading-7 text-sky-500 text-center mb-2">
            Step 3:
          </span>
          Common Mistakes to Avoid</h3>

        <div className="flex flex-col lg:flex-row justify-center items-stretch my-8 md:my-8 lg:my-16">

          <div className='cmtd  mb-8 mx-0 lg:mb-0 lg:mr-8 flex items-center justify-center'>
            <h4 className=' text-[#0F172A] text-2xl md:text-3xl font-bold tracking-tight'>What to Do</h4>
          </div>

          <ul className="bg-gray-900 p-0  grid  grid-cols-1 lg:grid-cols-[1fr_1fr_1fr] items-end justify-center gap-8">

            <li>

              <span className='flex flex-col px-4 g-style bg-[#274481]'>
                <span className="cmtd-icon text-center text-white">1</span>
                Take a clean full-screen screenshot by waiting for the game and text animations to complete.
              </span>
            </li>

            <li>
              <span className='flex flex-col px-4 g-style bg-[#2a4fa3]'>
                <span className="cmtd-icon text-center text-white">2</span>
                Set phone brightness to the maximum level.
              </span>


            </li>

            <li>

              <span className='flex flex-col px-4 g-style bg-[#2d60c8]'>
                <span className="cmtd-icon text-center text-white">3</span>
                Upload raw screenshots.
              </span>

            </li>

          </ul>

        </div>


        <div className="flex flex-col lg:flex-row justify-center items-stretch mb-8 md:mb-8 lg:mb-16 ">


          <div className='cmtd  mb-8 mx-0 lg:mb-0 lg:mr-8 flex items-center justify-center'>
            <h4 className=' text-[#0F172A] text-2xl md:text-3xl font-bold tracking-tight'>What to Avoid</h4>
          </div>


          <ul className="bg-gray-900 p-0  grid  grid-cols-1 lg:grid-cols-[1fr_1fr_1fr] items-end justify-center gap-8">



            <li>

              <span className='flex flex-col px-4 g-style bg-[#274481]'>
                <span className="cmtd-icon2 text-center text-white">1</span>
                The screenshot includes any overlays or effects of ad pop-ups, and game/loading animations visible.
              </span>
            </li>



            <li>

              <span className='flex flex-col px-4 g-style bg-[#274481]'>
                <span className="cmtd-icon2 text-center text-white">2</span>
                Keep phone brightness to the minimum level.
              </span>
            </li>


            <li>

              <span className='flex flex-col px-4 g-style bg-[#274481]'>
                <span className="cmtd-icon2 text-center text-white">3</span>
                Crop or edit the screenshot.
              </span>
            </li>









          </ul>






        </div>


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
