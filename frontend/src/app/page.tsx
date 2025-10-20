export default function Home() {
  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start w-full max-w-2xl">
        <h1 className="text-4xl font-bold text-center sm:text-left">
          Song Credits
        </h1>
        <p className="text-sm/6 text-center sm:text-left text-gray-600 dark:text-gray-400">
          Search for a playlist and see song credits.
        </p>

        <div className="flex w-full gap-4">
          <input
            type="text"
            placeholder="Search a playlist..."
            className="flex-1 rounded-lg border border-gray-300 dark:border-gray-700 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
          />
          <button className="bg-blue-500 text-white font-medium px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors">
            Search
          </button>
        </div>
      </main>

      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center text-sm text-gray-500 dark:text-gray-400">
        <span>&copy; {new Date().getFullYear()} Song Credits</span>
        <a
          href="#"
          className="hover:underline hover:underline-offset-4"
        >
          About
        </a>
      </footer>
    </div>
  );
}
