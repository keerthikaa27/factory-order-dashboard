export const isLoggedIn = (): boolean => {
  const token = localStorage.getItem("access_token");
  return !!token;
};

export const logout = () => {
  localStorage.removeItem("access_token");
};
