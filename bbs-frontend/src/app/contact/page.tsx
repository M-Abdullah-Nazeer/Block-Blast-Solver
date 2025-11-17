import { FC } from 'react'




// app/privacy-policy/page.tsx
// app/disclaimer/page.tsx
export const metadata = {
    title: 'Contact - Block Blast Solver',
    description: 'Send your query or feedback to us through email',
    openGraph: {
        title: 'Contact - Block Blast Solver',
        description: 'Contact us using email',
        url: 'https://blockblastsolverai.com/contact',
        siteName: 'Block Blast Solver',
        locale: 'en_US',
        type: 'website',
    },
    keywords: [
        'Block Blast Solver contact us',
        'Block Blast Solver email',
    ],
}







const page: FC = () => {
    return (

        <div className="text-slate-300">
            <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">


                <h1 className="text-2xl font-bold mb-4 text-slate-100">Contact Us</h1>

                <p className='mb-4'>If any screenshot is not proccessed by our AI system accurately or you get any kind of error while using this tool. Feel free to contact us through email. Our team will respond you within 72 hours. Make sure to attach screenshot of error or gameplay. Your feedback will help us to improve, Thanks!. </p>

                <ul className="list-disc ml-8 sm:ml-1 mb-4">
                    <li>Email: admin@blockblastsolverai.com</li>
                </ul>

            </div>
        </div>
    )

}

export default page;