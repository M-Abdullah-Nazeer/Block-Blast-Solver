import Link from 'next/link'
import { NavItem } from '@/src/types/nav'


import { cn } from '@/lib/utils'
import BlockBlastSolverLogo from "public/block-blast-solver-logo.webp"
import MenuIcon from "public/menu-icon.webp"
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

import { useTab } from '../context/TabContext';
import Image from 'next/image'


interface MainNavProps {
  items?: NavItem[]
}

export function MainNav({ items }: MainNavProps) {

  const { setActiveTab } = useTab();



  return (
    <div className="flex w-full gap-6 md:gap-10 items-center justify-between ">
      <Link href="/" className="hidden float-right items-center space-x-2 md:flex">

        <Image
          className="w-10 h-10"
          src={BlockBlastSolverLogo}
          alt="Block Blast Solver Logo"
          priority
          width={500}
          height={500}

        />


      </Link>
      {items?.length ? (
        <nav className="hidden gap-6 md:flex">
        
             
                <Link
               
                  href={items[0].href!}
                  className={cn(
                    'flex items-center text-lg font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-100 sm:text-sm',
                    items[0].disabled && 'cursor-not-allowed opacity-80'
                  )}
                  onClick={() => setActiveTab(1)}

                >
                   {items[0].title}
                </Link>
                <Link
               
                  href={items[1].href!}
                  className={cn(
                    'flex items-center text-lg font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-100 sm:text-sm',
                    items[1].disabled && 'cursor-not-allowed opacity-80'
                  )}
                  onClick={() => setActiveTab(2)}

                >
                   {items[1].title}
                </Link>
                <a
  href="https://play.google.com/store/apps/details?id=com.block.juggle&hl=en"
  target="_blank"
  rel="noopener noreferrer"
  className="flex items-center text-lg font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-100 sm:text-sm cursor-pointer opacity-80"
>
  Play Game
</a>

         
              <a
  href="privacy-policy"
  className="flex items-center text-lg font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-100 sm:text-sm cursor-pointer opacity-80"
>
Privacy Policy
</a>
             
              <a
                href="terms"
                className="flex items-center text-lg font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-100 sm:text-sm cursor-pointer opacity-80"
              >
              Terms
              </a>
             

              <a
  href="disclaimer"
  className="flex items-center text-lg font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-100 sm:text-sm cursor-pointer opacity-80"
>
Disclaimer
</a>
              
        

        </nav>



      ) : null}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            className="-ml-4 text-base hover:bg-transparent focus:ring-0 md:hidden"
          >
            <Image
              className="w-6 h-6"
              src={MenuIcon}
              alt="Menu Icon"
              priority
              width={24}
              height={24}
              sizes="24px"

            />

          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          align="start"
          sideOffset={24}
          className="w-[300px] overflow-scroll"
        >

          <DropdownMenuSeparator />
          {/* {
          items?.map(
            (item, index) =>
              item.href && ( */}

          {items?.length ? (
            <>
              <DropdownMenuItem asChild>
                <Link className='cursor-pointer' href={items[0].href!} onClick={() => setActiveTab(1)}>
                  {items[0].title}
                </Link>
              </DropdownMenuItem>
              <DropdownMenuItem asChild>
                <Link className='cursor-pointer' href={items[1].href!} onClick={() => setActiveTab(2)}>
                  {items[1].title}
                </Link>
              </DropdownMenuItem>
              <DropdownMenuItem asChild>
              <a
  href="https://play.google.com/store/apps/details?id=com.block.juggle&hl=en"
  target="_blank"
  rel="noopener noreferrer"
  className="flex items-center text-lg font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-100 sm:text-sm cursor-pointer opacity-80"
>
  Play Game
</a>
              </DropdownMenuItem>

              <DropdownMenuItem asChild>
              <a
  href="privacy-policy"
  className="flex items-center text-lg font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-100 sm:text-sm cursor-pointer opacity-80"
>
Privacy Policy
</a>
              </DropdownMenuItem>

              <DropdownMenuItem asChild>
              <a
  href="terms"
  className="flex items-center text-lg font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-100 sm:text-sm cursor-pointer opacity-80"
>
Terms
</a>
              </DropdownMenuItem>

              <DropdownMenuItem asChild>
              <a
  href="disclaimer"
  className="flex items-center text-lg font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-100 sm:text-sm cursor-pointer opacity-80"
>
Disclaimer
</a>
              </DropdownMenuItem>



            </>
          ) : null}


          {/* )
          )} */}
        </DropdownMenuContent>
      </DropdownMenu>
      <Image
        className="w-10 h-10 block md:hidden"
        src={BlockBlastSolverLogo}
        alt="Block Blast Solver Logo"
        priority
        width={500}
        height={500}

      />

    </div>
  )
}
