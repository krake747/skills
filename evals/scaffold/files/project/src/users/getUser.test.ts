import { getUser } from "./getUser";

test("returns a user", async () => {
  await expect(getUser("user-1")).resolves.toMatchObject({ status: 200 });
});
