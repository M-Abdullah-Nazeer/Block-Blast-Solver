import OGImage from "public/og-image.webp"
import HomePageComponent from "../components/HomePageComponent";
import { FC } from 'react';

export const metadata = {
  description: "Get Block Blast high score in 1 click. Upload screenshot and let block blast solver give you complete stepwise solution. Enjoy free unlimited attempts.",
  openGraph: {
    title: "Block Blast Solver - Instant Puzzle Solutions",
    description: "Block Blast Solver tool that analyzes Block Blast screenshots to generate optimal moves",
    url: "https://blockblastsolverai.com",
    type: "website",
    images: [{
      url: OGImage.src,
      width: 1076,
      height: 428,
      alt: "Block Blast Cheat",
    }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Block Blast Solver",
    description: "Free Block Blast Solver for Quick Solutions",
    images: [{  
      url: OGImage.src,
      width: 1076,
      height: 428,
      alt: "Block Blast Cheat",
    }]
  },
};

const Page: FC = () => {
  
  return (
<HomePageComponent/>
  )
}

export default Page
