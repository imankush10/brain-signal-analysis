import { Link } from "react-router-dom";
import NavBar from "./NavBar";

export default function Homepage() {
  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <NavBar />
      <section className="w-full py-12 lg:py-16 px-4 text-black">
        <div className="container grid gap-6 px-4 md:px-6 lg:grid-cols-2 lg:gap-12">
          <div className="flex items-center justify-center">
            <img
              src="https://images.unsplash.com/photo-1557672186-269926e526c1?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              width="550"
              height="550"
              alt="Brain"
              className="mx-auto aspect-square overflow-hidden rounded-xl object-cover"
            />
          </div>
          <div className="flex flex-col justify-center space-y-4">
            <div className="space-y-2">
              <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">
                Brain Attention Metrics: Objective, Accurate, and Actionable
              </h1>
              <p className="max-w-[600px] text-muted-foreground md:text-lg">
                Our EEG-based AI model provides unparalleled insights into
                cognitive focus, helping individuals, educators, and
                organizations optimize performance and productivity.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}