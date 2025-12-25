import OGImage from "public/og-image.webp"
import HomePageComponent from "../components/HomePageComponent";
import { FC } from 'react';

export const metadata = {
  description: "Get Block Blast high score in 1 click. Upload screenshot and let our AI solver give you step-by-step solution. Enjoy free unlimited attempts.",
  openGraph: {
    title: "Block Blast Solver - Instant Puzzle Solutions",
    description: "AI-powered tool that analyzes Block Blast screenshots to generate optimal moves",
    url: "https://blockblastsolverai.com",
    type: "website",
    images: [{
      url: OGImage.src,
      width: 1076,
      height: 428,
      alt: "AI Block Blast cheat",
    }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Block Blast Solver AI",
    description: "Free AI-powered solution generator for Block Blast puzzles",
    images: [{  
      url: OGImage.src,
      width: 1076,
      height: 428,
      alt: "AI Block Blast cheat",
    }]
  },
};

const Page: FC = () => {
  
  return (
<HomePageComponent/>
  )
}

export default Page
