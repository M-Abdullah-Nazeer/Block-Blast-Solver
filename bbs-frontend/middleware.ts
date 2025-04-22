import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
    const url = request.nextUrl;

    // Redirect HTTP to HTTPS
    if (url.protocol === 'http:') {
        return NextResponse.redirect(
            new URL(`https://${url.hostname}${url.pathname}`),
            301
        );
    }

    // Proceed with normal response and add security headers
    const response = NextResponse.next();
    response.headers.set('X-Content-Type-Options', 'nosniff');
    response.headers.set('X-Frame-Options', 'SAMEORIGIN');
    response.headers.set('X-XSS-Protection', '1; mode=block');

    return response;
}

// Apply to all routes
export const config = {
    matcher: '/:path*',
};
