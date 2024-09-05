import { Link } from "react-router-dom";

function NavBar() {
  return (
    <nav className="bg-blue-900 text-white p-4 px-8 flex justify-between">
      <Link className="font-bold text-2xl" to="/">
        FocusFinder
      </Link>
      <ul className="flex items-center space-x-4">
        <li>
          <Link
            to="/upload"
            className="bg-neutral-200 text-gray-900 font-bold px-4 py-2 rounded-md transition duration-300 hover:bg-gray-300"
          >
            Get Started
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default NavBar;
