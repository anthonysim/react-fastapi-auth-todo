export const fakeRegister = (
  email: string,
  password: string
): Promise<{
  message: string;
  user: { id: number; email: string };
}> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log("Fake register with:", email, password);
      resolve({
        message: "User registered successfully",
        user: {
          id: 1,
          email: "example1@gmail.com",
        },
      });
    }, 2000);
  });
};
