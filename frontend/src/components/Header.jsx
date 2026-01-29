export default function Header(){
  return(
    <header style={{
      padding: '5px 30px',
      background: '#000',
      borderBottom: '1px solid #1a1a1a',
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
    }}>
      <h1 style={{color:"green", margin:0, letterSpacing:"7px"}}>PHONK UNIVERSE</h1>
      <h1 style={{color:"#666"}}>Ultimate xs</h1>
    </header>
  );
}