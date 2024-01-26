const Blob = () => {
  return (
    <div
      style={{
        zIndex: "-1",
        position: "absolute",
        top: "50%",
        left: "50%",
        height: "40vw",
        width: "40vw",
        transform: "translate(-50%, -50%)",
        background: "#da2909",
        animation: `animate-blob 20s linear infinite`,
        borderRadius: "45% 55% 70% 35% / 70% 30% 90% 40%",
      }}
    >
      <style>
        {`
          @keyframes animate-blob {
            0%, 100% {
              border-radius: 45% 55% 70% 35% / 70% 30% 90% 40%;
              transform: translate(-50%, -50%);
            }

            25% {
              border-radius: 55% 45% 30% 35% / 50% 30% 60% 10%;
              transform: translate(-50%, -50%) rotate(90deg);
            }
            50% {
              border-radius: 65% 35% 35% 65% / 40% 60% 30% 70%;
              transform: translate(-50%, -50%) rotate(180deg);
            }
            75% {
              border-radius: 35% 65% 60% 40% / 70% 30% 40% 60%;
              transform: translate(-50%, -50%) rotate(270deg);
            }
          }
        `}
      </style>
    </div>
  );
};

export default Blob;
