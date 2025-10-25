
'use client'
import { FC, useEffect, useState } from 'react'
import { Button, buttonVariants } from '@/ui/button'
import { FileInput } from '@/ui/file-input'
import FillManual from '@/components/fill-manual'
import incompleteAnimation from "public/incomplete-animation.webp"
import croppedScreenshot from "public/cropped-screenshot.webp"
import accurateScreenshot from "public/accurate-screenshot.webp"
import animationOnShapes from "public/animation-on-shapes.webp"
import gameScreenshot from "public/block-blast-game-screenshot.webp"
import AndroidLogo from "public/android-logo.webp"
import AppleLogo from "public/apple-logo.webp"
import LiteYouTubeEmbed from "react-lite-youtube-embed";
import "react-lite-youtube-embed/dist/LiteYouTubeEmbed.css";
import solvePlay from "public/solve-play.webp"
import uploadDraw from "public/upload-draw.webp"
import manualIcon from "public/manual-icon.png"
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import Image from 'next/image'
import { useTab } from '../context/TabContext';
import { ArticleSchema } from '../components/ArticleSchema'
import FinalOutput from '../components/FinalOutput'
import { Step } from "../types/steps"

const HomePageComponent = () => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const { activeTab, setActiveTab } = useTab();
  const [fmSolved, setFmSolved] = useState(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {

 
    if (activeTab === 1) {
      setFmSolved(false);
    } else if (activeTab === 2) {
      setUploadedFile(null);
    }
    setHideComp(activeTab === 3);
  }, [activeTab]);

  const clearFile = () => {
    if (activeTab > 1 && uploadedFile) {
      setActiveTab((activeTab - 2) as 1 | 2 | 3);
      setFmSolved(false);
    }
    if (activeTab > 1 && fmSolved) {
      setActiveTab((activeTab - 1) as 1 | 2 | 3);
      setFmSolved(true);
    }
    setUploadedFile(null);
    setHideComp((prev) => !prev);
  }

  const [hideComp, setHideComp] = useState(false);
  const [steps, setSteps] = useState<Step[]>([]);
  const [shapeColors, setShapeColors] = useState<Record<string, string>>({});

  const handleUploadSuccess = (
    receivedSteps: Step[],
    receivedShapeColors: Record<string, string>
  ) => {
    setSteps(receivedSteps);
    setShapeColors(receivedShapeColors);
    setHideComp((prev) => !prev);
  };
  const [activeIndex, setActiveIndex] = useState(-1);
  const faqs = [
    {
      question: 'How does the Block Blast game work?',
      answer: "It's a puzzle game that challenges the player's ability to find suitable positions on the grid for given shapes. A grid has an 8x8 structure consisting of 8 rows and 8 columns, while shapes can be simple or complex, e.g., L, T, square, rectangle shapes. As the game continues, the difficulty increases with more difficult puzzle levels and complex shapes. If by placing the shape on a grid any row or column gets completed, the user earns a score for that."
    },
    {
      question: 'How to get a really high score in Block Blast?',
      answer: 'Achieving a high score requires implementing effective strategies. Try to create chain reactions that open up opportunities for future moves. Consistently planning your shape placements in advance can trigger cascading effects, helping you maintain high scores. Remember, your high score is based on clearing the maximum number of rows or columns using the given shapes.'
    },
    {
      question: 'What is a Block Blast Solver?',
      answer: "It's a free online tool that provides unlimited help to decide on shape placement order after pattern recognition of blocks on the grid for the players. It requires simply a single image from the current gameplay of the player. There are no restrictions on the attempts, so upload as many images as you want for assistance, but one for each streak."
    },
    {
      question: 'How to get a Block Blast Solver?',
      answer: 'If you prefer using a laptop or computer for picture solver you can find our website-based tool using any search engine like Google. Or you can download free and install our app from the Play Store for Android and the App Store for iOS.'
    },
  ];

  const toggleAccordion = (index: number) => {
    setActiveIndex(prev => prev === index ? -1 : index);
  };
  const background = `radial-gradient(650px circle at 250px 250px, rgba(14, 165, 233, 0.15), transparent 80%)`;
  return (
    <>
      <ArticleSchema />
      <div className='relative container'>
        <section className="w-full grid items-center lg:gap-8 gap-6 pt-6 pb-0 md:pt-10">
          <div className="container flex w-full  flex-col items-center gap-2">
            <h1 className="text-[40px] font-extrabold leading-tight tracking-tighter sm:text-3xl md:text-5xl lg:text-6xl text-center">
              Block Blast Solver
            </h1>
          </div>
          {/* Try Another Button */}
          {(uploadedFile || fmSolved) && (
            <Tooltip>
              <TooltipTrigger asChild>
                <div className="flex justify-center w-full my-4">
                  <Button
                    disabled={!(uploadedFile || fmSolved)}
                    className={buttonVariants({
                      size: "lg",
                      className: "w-fit hover:!bg-[#468beb] hover:!text-white cursor-pointer"
                    })}
                    onClick={clearFile}
                  >
                    Try Another
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-rotate-cw ml-1"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8" /><path d="M21 3v5h-5" /></svg>
                  </Button>
                </div>
              </TooltipTrigger>
              <TooltipContent className="!bg-[#316edf] !text-white">
                <p>Get results for next move</p>
              </TooltipContent>
            </Tooltip>
          )}

          {/* Upload Section */}
          {(activeTab === 1 && !fmSolved) &&
            <div className={`${hideComp ? "hidden" : "flex"} flex-col lg:flex-row md:flex-row gap-4 lg:gap-20 justify-center items-stretch bg-[#0088cc17] border border-white/10 py-8 px-2 lg:p-10 rounded-lg z-10 container`}>
              {isLoading ? (
                <div className="flex justify-center items-center h-32">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
                </div>
              ) : (
                <>
                  <FileInput uploadedFile={uploadedFile} setIsLoading={setIsLoading} setUploadedFile={setUploadedFile} onUploadSuccess={handleUploadSuccess} />
                  <div className="flex flex-col justify-center items-center gap-4 w-full lg:w-1/2 md:w-1/2 bg-[#0f172d] rounded-lg py-8 px-2 lg:p-10 border-4 border-[#9ac8f6] border-solid">
                    <Image
                      src={gameScreenshot}
                      alt="gameplay screenshot"
                      width={150}
                      height={331}
                      className="rounded-lg w-[150px] h-[331px]"
                      sizes="150px"
                      priority

                    />
                    <span>OR</span>
                    <button className="flex items-center justify-center gap-3 bg-slate-50  text-slate-900 p-[16px] lg:px-[24px] lg:py-[16px] rounded-lg hover:bg-slate-100 transition-all duration-300 ease-in-out w-[200px] lg:w-[252px] h-[56px] cursor-pointer" onClick={() => setActiveTab(2)}>
                      <Image priority alt="fill manually icon" className="w-[32px] h-[32px] aspect-square" src={manualIcon} width={32} height={32} sizes="32px" />
                      <span className="text-18px font-semibold leading-24px text-center">Fill Manually</span>
                    </button>
                  </div>
                </>
              )}
            </div>
          }
          {(activeTab === 2 && !uploadedFile) &&
            <div className={`${hideComp ? "hidden" : "flex"} flex-col lg:flex-row  gap-4 lg:gap-20 justify-center items-center lg:items-start bg-[#0088cc17] border border-white/10 py-8 px-2 lg:p-10 rounded-lg z-10 container`}>
              <FillManual handleUploadSuccess={handleUploadSuccess} setFmSolved={setFmSolved} />
            </div>
          }
          {(uploadedFile || fmSolved) && (activeTab === 3) && (
            <FinalOutput steps={steps} shapeColors={shapeColors} />
          )}
          {(uploadedFile) && (
            <div className="flex flex-col justify-center items-center">
              <p className='text-white text-lg font-bold my-5'>Uploaded Screenshot</p>
              <Image
                src={URL.createObjectURL(uploadedFile)}
                alt="Uploaded Image Preview"
                loading='lazy'
                width={1080}
                height={2400}
                className="object-cover rounded-lg mx-auto mb-2 lg:w-1/6 lg:h-[auto] md:w-1/4 sm:w-full md:h-[auto]"
              />
            </div>
          )}
          <div className='pt-24 z-10'>
            <div className="container flex w-full flex-col items-start gap-2 ">
              <p className="text-base leading-7 text-gray-300 ">
                <strong>It&apos;s an AI-based problem solver</strong> that finds the best possible moves for a Block Blast game using just a screenshot of your gameplay. You can achieve a high score in the game with a single click using our free online tool.
              </p>
              <p className="text-base leading-7 text-gray-300 ">
                What makes it better than other helpers is its advanced solver algorithms. Block Blast Solver finds the best possible steps to take to maximize your score in a given situation.
              </p>
              <p className="text-base leading-7 text-gray-300 ">
                Also, its solution helps you understand the right place for the right shape with the help of 3D design and colors. Unlike others, this online solver represents each shape with its original color for a better understanding of the player, which makes it the best.
              </p>
            </div>
          </div>
        </section>
        <section className='pt-24'>
          <h2 className='text-4xl text-sky-500 font-bold tracking-tight text-center'>How to Use <strong className='mark'>Block Blast Solver?</strong></h2>
          <p className='mt-6 text-base leading-7 text-gray-300 text-center'>You only need to upload 1 picture for each step, however, be sure to follow these steps to get accurate results. Otherwise, the Block Blast AI solver will not be able to help you with cheat moves.</p>
          <div className=" p-0 md:p-8 grid  grid-cols-1 md:grid-cols-[1fr_2fr] items-center justify-center gap-8 md:gap-[20px] lg:gap-[50px] xl:gap-[100px]">
            <div className="group relative max-w-md rounded-xl border border-white/10 lg:px-8 md:px-6 p-4 md:py-8 lg:py-16 shadow-2xl"
            >
              <div
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
        <section className='step2 pt-24 my-0 pb-0'>
          <h3 className='text-2xl md:text-3xl font-bold tracking-tight text-white text-center h3-cust'>
            <span className="text-base font-semibold leading-7 text-sky-500 text-center mb-2">
              Step 2:
            </span>
            Take the Screenshot</h3>
          <div className="px-0 py-0 md:px-8 grid  grid-cols-1 lg:grid-cols-[1fr_1fr] items-start justify-center gap-8 my-0">
            <details className="group relative rounded-xl border border-white/10  lg:px-8 md:px-6 p-0 md:py-8 lg:py-16 shadow-2xl"
            >
              <summary><h4>For Android</h4>
                <Image
                  src={AndroidLogo}
                  alt="Android logo"
                  loading='lazy'
                  width={500}
                  height={500}
                  className="w-6 h-6 ml-1"
                />
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
            <details className="group relative rounded-xl border border-white/10  lg:px-8 md:px-6 p-0 md:py-8 lg:py-16 shadow-2xl">
              <summary><h4>For iPhone</h4>
                <Image
                  src={AppleLogo}
                  alt="Iphone logo"
                  loading='lazy'
                  width={500}
                  height={500}
                  className="w-6 h-6 ml-1"
                />
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
        <section className='pt-24'>
          <h3 className='text-2xl md:text-3xl font-bold tracking-tight text-white text-center h3-cust'>
            <span className="text-base font-semibold leading-7 text-sky-500 text-center mb-2">
              Step 3:
            </span>
            Common Mistakes to Avoid</h3>
          <div className="flex flex-col lg:flex-row justify-center items-stretch my-8 md:my-8 lg:my-16">
            <div className='cmtd  mb-8 mx-0 lg:mb-0 lg:mr-8 flex items-center justify-center'>
              <h4 className=' text-[#0F172A] text-2xl md:text-3xl font-bold tracking-tight'>What to Do</h4>
            </div>
            <ul className=" p-0  grid  grid-cols-1 lg:grid-cols-[1fr_1fr_1fr] items-end justify-center gap-8">
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
            <ul className=" p-0  grid  grid-cols-1 lg:grid-cols-[1fr_1fr_1fr] items-end justify-center gap-8">
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
              </li></ul></div>
        </section>
        <section className='py-24'>
          <h3 className='text-2xl md:text-3xl font-bold tracking-tight text-white text-center h3-cust'>
            <span className="text-base font-semibold leading-7 text-sky-500 text-center mb-2">
              Step 4:
            </span>
            Screenshot Examples</h3>
          <div className="flex flex-col md:flex-row justify-center items-center py-4 gap-8 mt-6">
            <div>
              <h4 className='mb-2 text-center'>✔️ Valid Capture</h4>
              <figure>
                <Image className='mx-auto md:w-full w-[150px] h-auto'
                  src={accurateScreenshot}
                  alt="puzzle game accurate screenshot"
                  width={580}
                  height={1280}
                  sizes="(max-width: 640px) 150px, 580px"
                  loading="lazy"
                />
                <figcaption>Accurate screenshot</figcaption>
              </figure>
            </div>
            <div>
              <h4 className='mb-2'>❌ Invalid Captures</h4>
              <div className="grid  grid-cols-1 md:grid-cols-[1fr_1fr_1fr] items-center lg:items-start justify-center gap-8">
                <figure>
                  <Image
                    className='md:w-full w-[150px] h-auto'
                    src={incompleteAnimation}
                    alt="screenshot with incomplete aimation"
                    width={580}
                    height={1280}
                    sizes="(max-width: 640px) 150px, 580px"
                    loading="lazy"
                  />
                  <figcaption>Incomplete animation</figcaption>
                </figure>
                <figure>
                  <Image
                    className='md:w-full w-[150px] h-auto'
                    src={animationOnShapes}
                    alt="screenshot with animation covering shapes"
                    width={580}
                    height={1280}
                    sizes="(max-width: 640px) 150px, 580px"
                    loading="lazy"
                  />
                  <figcaption>Animation on shapes</figcaption>
                </figure>
                <figure>
                  <Image
                    className='md:w-full w-[150px] h-auto'
                    src={croppedScreenshot}
                    alt="modified screenshot"
                    width={580}
                    height={1280}
                    sizes="(max-width: 640px) 150px, 580px"
                    loading="lazy"
                  />
                  <figcaption>Cropped screenshot</figcaption>
                </figure>
              </div>
            </div>
          </div>
        </section>
        <section>
          <div className="grid  grid-cols-1 lg:grid-cols-[1fr_1fr] items-center lg:items-start justify-center gap-8">
            <div className="group fixed-style2 relative max-w-md rounded-xl border border-white/10  lg:px-8 md:px-6 p-4 md:py-8 lg:py-16 shadow-2xl  mt-0 lg:mt-[75px] justify-self-center lg:justify-self-end"
            >
              <div>
                <div className="mt-2 flex items-center gap-x-2">
                  <h3 className="text-2xl md:text-3xl font-bold tracking-tight text-white h3-cust">
                    <span className="text-base font-semibold leading-7 text-sky-500 mb-2">
                      Step 1:
                    </span>
                    Upload Or Draw
                  </h3>
                </div>
                <p className="mt-6 text-base leading-7 text-gray-300">
                  Click the upload button and select a screenshot from your device, or you can manually draw your shapes and board. Once the upload is completed, then an algorithm that is specifically designed for this game will find solutions automatically, just wait a few seconds for a response.
                </p>
              </div>
            </div>
            <Image
              className="rounded-xl max-w-md w-full object-cover border border-white/10  justify-self-center lg:justify-self-start"
              src={uploadDraw}
              alt="Block Blast Solver Features"
              loading="lazy"
              width={448}
              height={448}
              sizes="(max-width: 448px) 100vw, 448px"
            />
          </div>
          <div className="flex flex-col-reverse lg:grid lg:grid-cols-[1fr_1fr] items-center lg:items-start justify-center gap-8">
            <Image
              className="rounded-xl max-w-md w-full object-cover border border-white/10 justify-self-center lg:justify-self-end  mt-0 lg:mt-[75px]"
              src={solvePlay}
              alt="screenshot solver"
              loading="lazy"
              width={448}
              height={448}
              sizes="(max-width: 448px) 100vw, 448px"
            />
            <div className="group relative max-w-md fixed-style rounded-xl border border-white/10  lg:px-8 md:px-6 p-4 md:py-8 lg:py-16 shadow-2xl  justify-self-center lg:justify-self-start lg:mt-[0px] mt-8"
            >
              <div>
                <div className="mt-2 flex items-center gap-x-2">
                  <h3 className="text-2xl md:text-3xl font-bold tracking-tight text-white h3-cust">
                    <span className="text-base font-semibold leading-7 text-sky-500 mb-2">
                      Step 1:
                    </span>
                    Solve and play
                  </h3>
                </div>
                <p className="mt-6 text-base leading-7 text-gray-300">
                  The final output of the combo solver will contain all 3 steps with solutions. Each shape will be placed in a position that maximizes your score or sets up the next move for a high-scoring play. Completed rows or columns will be highlighted using a green border. Each shape in the output will retain the same color and form as it has in the uploaded screenshot.
                </p>
              </div>
            </div>
          </div>
        </section>
        <section className="py-24" aria-label="Why Choose Block Blast Solver Section">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="mb-16">
              <h2 className="text-4xl md:text-4xl font-bold tracking-tight text-white text-center">
                Why Choose Block Blast Solver?
              </h2>
              <p className="mt-6 text-base leading-7 text-gray-300 text-center">
                We know you are good at block blast, but do you want to be best?. Choose our solver to save time and avoid mental exercise.
              </p>
              <div className="flex flex-col-reverse lg:grid lg:grid-cols-3 items-stretch justify-center gap-12 mt-12">
                <div className="h-full flex flex-col justify-between col-span-2">
                  <div className="flex flex-col lg:flex-row items-center lg:items-start justify-center">
                    <div className="mb-5 flex  items-start justify-center">
                      <svg viewBox="0 0 24 24" className="w-8 h-8 text-[#0ea5e9]" xmlns="http://www.w3.org/2000/svg">
                        <path fill='currentColor' d="M12.0003 3C17.3924 3 21.8784 6.87976 22.8189 12C21.8784 17.1202 17.3924 21 12.0003 21C6.60812 21 2.12215 17.1202 1.18164 12C2.12215 6.87976 6.60812 3 12.0003 3ZM12.0003 19C16.2359 19 19.8603 16.052 20.7777 12C19.8603 7.94803 16.2359 5 12.0003 5C7.7646 5 4.14022 7.94803 3.22278 12C4.14022 16.052 7.7646 19 12.0003 19ZM12.0003 16.5C9.51498 16.5 7.50026 14.4853 7.50026 12C7.50026 9.51472 9.51498 7.5 12.0003 7.5C14.4855 7.5 16.5003 9.51472 16.5003 12C16.5003 14.4853 14.4855 16.5 12.0003 16.5ZM12.0003 14.5C13.381 14.5 14.5003 13.3807 14.5003 12C14.5003 10.6193 13.381 9.5 12.0003 9.5C10.6196 9.5 9.50026 10.6193 9.50026 12C9.50026 13.3807 10.6196 14.5 12.0003 14.5Z"></path>
                      </svg>
                    </div>
                    <div className="ml-0 lg:ml-6 flex flex-col items-center lg:items-start justify-center">
                      <h3 className="mb-2 text-white font-extrabold ">3D Color Visualization</h3>
                      <p className="text-base leading-7 text-gray-300 text-center lg:text-start">
                        The final output of the solver will contain all 3 steps with 3D visualization of solutions. This better design gives us an edge above all other tools, making user experience better.
                      </p>
                    </div>
                  </div>
                  <div className="mt-6 flex flex-col lg:flex-row items-center lg:items-start justify-center">
                    <div className="mb-5 flex items-start justify-center">
                      <svg viewBox="0 0 24 24" className="w-8 h-8 text-[#0ea5e9]" xmlns="http://www.w3.org/2000/svg">
                        <path fill='currentColor' d="M5.46257 4.43262C7.21556 2.91688 9.5007 2 12 2C17.5228 2 22 6.47715 22 12C22 14.1361 21.3302 16.1158 20.1892 17.7406L17 12H20C20 7.58172 16.4183 4 12 4C9.84982 4 7.89777 4.84827 6.46023 6.22842L5.46257 4.43262ZM18.5374 19.5674C16.7844 21.0831 14.4993 22 12 22C6.47715 22 2 17.5228 2 12C2 9.86386 2.66979 7.88416 3.8108 6.25944L7 12H4C4 16.4183 7.58172 20 12 20C14.1502 20 16.1022 19.1517 17.5398 17.7716L18.5374 19.5674Z"></path>
                      </svg>
                    </div>
                    <div className="ml-0 lg:ml-6 flex flex-col items-center lg:items-start justify-center">
                      <h3 className="mb-2 text-white font-extrabold">Updates & Feedback</h3>
                      <p className="text-base leading-7 text-gray-300 text-center lg:text-start">
                        It is independent from game updates; no matter how much the game changes, it will work. We also improve our AI based on user feedback.
                      </p>
                    </div>
                  </div>
                  <div className="mt-6 flex flex-col lg:flex-row items-center lg:items-start justify-center">
                    <div className="mb-5 flex items-start justify-center">
                      <svg viewBox="0 0 24 24" className="w-8 h-8 text-[#0ea5e9]" xmlns="http://www.w3.org/2000/svg">
                        <path fill='currentColor' d="M9 4C10.1046 4 11 4.89543 11 6V12.8271C10.1058 12.1373 8.96602 11.7305 7.6644 11.5136L7.3356 13.4864C8.71622 13.7165 9.59743 14.1528 10.1402 14.7408C10.67 15.3147 11 16.167 11 17.5C11 18.8807 9.88071 20 8.5 20C7.11929 20 6 18.8807 6 17.5V17.1493C6.43007 17.2926 6.87634 17.4099 7.3356 17.4864L7.6644 15.5136C6.92149 15.3898 6.1752 15.1144 5.42909 14.7599C4.58157 14.3573 4 13.499 4 12.5C4 11.6653 4.20761 11.0085 4.55874 10.5257C4.90441 10.0504 5.4419 9.6703 6.24254 9.47014L7 9.28078V6C7 4.89543 7.89543 4 9 4ZM12 3.35418C11.2671 2.52376 10.1947 2 9 2C6.79086 2 5 3.79086 5 6V7.77422C4.14895 8.11644 3.45143 8.64785 2.94126 9.34933C2.29239 10.2415 2 11.3347 2 12.5C2 14.0652 2.79565 15.4367 4 16.2422V17.5C4 19.9853 6.01472 22 8.5 22C9.91363 22 11.175 21.3482 12 20.3287C12.825 21.3482 14.0864 22 15.5 22C17.9853 22 20 19.9853 20 17.5V16.2422C21.2044 15.4367 22 14.0652 22 12.5C22 11.3347 21.7076 10.2415 21.0587 9.34933C20.5486 8.64785 19.8511 8.11644 19 7.77422V6C19 3.79086 17.2091 2 15 2C13.8053 2 12.7329 2.52376 12 3.35418ZM18 17.1493V17.5C18 18.8807 16.8807 20 15.5 20C14.1193 20 13 18.8807 13 17.5C13 16.167 13.33 15.3147 13.8598 14.7408C14.4026 14.1528 15.2838 13.7165 16.6644 13.4864L16.3356 11.5136C15.034 11.7305 13.8942 12.1373 13 12.8271V6C13 4.89543 13.8954 4 15 4C16.1046 4 17 4.89543 17 6V9.28078L17.7575 9.47014C18.5581 9.6703 19.0956 10.0504 19.4413 10.5257C19.7924 11.0085 20 11.6653 20 12.5C20 13.499 19.4184 14.3573 18.5709 14.7599C17.8248 15.1144 17.0785 15.3898 16.3356 15.5136L16.6644 17.4864C17.1237 17.4099 17.5699 17.2926 18 17.1493Z"></path>
                      </svg>
                    </div>
                    <div className="ml-0 lg:ml-6 flex flex-col items-center lg:items-start justify-center">
                      <h3 className="mb-2 text-white font-extrabold">Optimal Strategical Solutions</h3>
                      <p className="text-base leading-7 text-gray-300 text-center lg:text-start">
                        Assume it like an experienced senior player, calculating the best perfect possible moves in a given round — just to maximize block clearance.
                      </p>
                    </div>
                  </div>
                  <div className="mt-6 flex flex-col lg:flex-row items-center lg:items-start justify-center">
                    <div className="mb-5 flex items-start justify-center">
                      <svg viewBox="0 0 24 24" className="w-8 h-8 text-[#0ea5e9]" xmlns="http://www.w3.org/2000/svg">
                        <path fill='currentColor' d="M20.7134 8.12811L20.4668 8.69379C20.2864 9.10792 19.7136 9.10792 19.5331 8.69379L19.2866 8.12811C18.8471 7.11947 18.0555 6.31641 17.0677 5.87708L16.308 5.53922C15.8973 5.35653 15.8973 4.75881 16.308 4.57612L17.0252 4.25714C18.0384 3.80651 18.8442 2.97373 19.2761 1.93083L19.5293 1.31953C19.7058 0.893489 20.2942 0.893489 20.4706 1.31953L20.7238 1.93083C21.1558 2.97373 21.9616 3.80651 22.9748 4.25714L23.6919 4.57612C24.1027 4.75881 24.1027 5.35653 23.6919 5.53922L22.9323 5.87708C21.9445 6.31641 21.1529 7.11947 20.7134 8.12811ZM2.9918 3H14V5H4V19L14 9L20 15V11H22V20.0066C22 20.5552 21.5447 21 21.0082 21H2.9918C2.44405 21 2 20.5551 2 20.0066V3.9934C2 3.44476 2.45531 3 2.9918 3ZM20 17.8284L14 11.8284L6.82843 19H20V17.8284ZM8 11C6.89543 11 6 10.1046 6 9C6 7.89543 6.89543 7 8 7C9.10457 7 10 7.89543 10 9C10 10.1046 9.10457 11 8 11Z"></path>
                      </svg>
                    </div>
                    <div className="ml-0 lg:ml-6 flex flex-col items-center lg:items-start justify-center">
                      <h3 className="mb-2 text-white font-extrabold">Faultless Block Recognition</h3>
                      <p className="text-base leading-7 text-gray-300 text-center lg:text-start">
                        Our solver has been through many rigorous testing phases. Because of that it detects blocks perfectly under any kind of conditions.
                      </p>
                    </div>
                  </div>
                </div>
              <div className="h-full w-full col-span-1">
                <div className="w-full h-full rounded-lg shadow-lg overflow-hidden ytb-article">
                  <LiteYouTubeEmbed
                    id="NUGkDWUnAN4"
                    title="Block Blast Solver Demo"
                    poster="maxresdefault"
                  />
                </div>
              </div>
              </div>
            </div>
          </div>
        </section>
        <section className="pb-24" aria-label="FAQ Section">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="mb-16">
              <h2 className='text-4xl md:text-4xl font-bold tracking-tight text-white text-center'> Frequently Asked<span className='text-sky-500'> Questions</span></h2>
              <p className='mt-6 text-base leading-7 text-gray-300 text-center'>Discover tips, tricks and hacks for the Block Blast game. Whether you&apos;re a newbie or a pro player, quickly get clear information with our frequently asked question&apos;s answers.</p>
            </div>
            <div className="accordion-group">
              {faqs.map((faq, index) => (
                <div
                  key={index}
                  className={`accordion border border-solid cursor-pointer border-white/10 p-4 rounded-xl transition duration-500 mb-8 lg:p-4 ${activeIndex === index ? 'active' : ''
                    }`}
                >
                  <div
                    role="button"
                    className="group inline-flex items-center justify-between text-left text-lg font-normal leading-8 w-full transition duration-500 ease-in-out"
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
                  </div>
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
      </div>
    </>
  )
}
export default HomePageComponent;