import type { Metadata } from 'next';
// import './globals.css';

declare module 'next' {
	interface Config {
		unstable_runtimeJS?: boolean;
	}
}

export const metadata: Metadata = {
	title: 'Prism',
	description: 'Prism scam detection tools'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
	return (
		<html lang='en'>
			<body>{children}</body>
		</html>
	);
}
