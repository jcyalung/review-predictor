"use client";
import { usePathname } from "next/navigation";
const routes = ['about', 
                'predictor',
                'recent',
                'statistics'];
export default function Header() {
  const pathname = usePathname();
  const active = pathname?.split('/')[1].toLowerCase() || 'home';
    return (
    <div className="header-center">
      <h1 className="heading1">Senti-IMDB</h1>
      <h2 className="heading2">Predict movie rating sentiment based on written IMDB reviews</h2>
      <ul className="navlist">
        {routes.map((route, index) => {
          return (
            <li 
            key={route}
            className={
              active === route ? 'navbar-active' : 'navbar'
            }><a href={route.toLowerCase()}>{route}</a></li>
          )
        })}
      </ul>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
      </footer>
    </div>
    )
}