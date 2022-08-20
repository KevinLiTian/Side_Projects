import { card } from "../assets";
import styles, { layout } from "../styles";
import Button from "./Button.jsx";

const CardDeal = () => (
  <section className={layout.section}>
    <div className={layout.sectionInfo}>
      <h2 className={styles.heading2}>
        Find a better card deal <br className="sm:block hidden" />
        in few easy steps.
      </h2>
      <p className={`${styles.paragraph} max-w-[470px] mt-5`}>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Sit amet cursus sit
        amet. Cras sed felis eget velit aliquet sagittis id consectetur.
        Maecenas volutpat blandit aliquam etiam erat velit scelerisque.
        Ullamcorper eget nulla facilisi etiam. Turpis egestas maecenas pharetra
        convallis.
      </p>
      <Button styles="mt-10" />
    </div>
    <div className={layout.sectionImg}>
      <img src={card} alt="card" className="w-[100%] h-[100%] object-contain" />
    </div>
  </section>
);

export default CardDeal;
