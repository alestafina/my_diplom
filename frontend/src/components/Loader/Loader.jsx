import classes from './Loader.module.css'; // Для стилей

const Loader = () => {
  return (
    <div className={classes.load}>
      <div className={classes.loader}></div>
    </div>
  );
};

export default Loader;
