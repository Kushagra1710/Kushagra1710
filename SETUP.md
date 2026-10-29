# Animated profile setup

The README appears on the profile when this branch is merged into `main` of the public `Kushagra1710/Kushagra1710` repository.

1. Extract the ZIP and upload its contents to the root of your profile repository. Include the hidden `.github/workflows/update-profile-art.yml` file. You can create a branch and pull request on GitHub if you want to review before publishing.
2. Check **Actions → Update profile art**. The first push should generate the portrait and real contribution calendar. If Actions are disabled, enable them, merge, then use **Run workflow** on `main`.
3. Commit to `main`, or merge your pull request when satisfied. Scheduled updates run daily at approximately 11:47 AM India time (06:17 UTC); GitHub may delay scheduled jobs.

The initial committed SVGs explicitly show a pending calendar and a KS monogram until the workflow succeeds. These are not simulated statistics or a fabricated portrait. No personal access token needs to be added. Repository policy must allow the built-in workflow token to write contents.

## Local commands

```sh
python -m pip install Pillow==11.3.0
python scripts/build_profile.py
# Or supply a cropped photo:
python scripts/build_profile.py --photo photo.jpg
```

The default portrait comes from the account's public GitHub avatar. Change the script or workflow if you prefer a permanent custom source photo. SVG animations have a reduced-motion alternative and their base state remains visible in renderers without animation support.

The contribution fetcher depends on GitHub's public HTML markup. It fails rather than publishing empty or partial statistics if parsing changes. A failed workflow leaves the previously committed artwork intact. Contribution totals reflect the days and counts publicly exposed by GitHub, not private activity that the account has chosen to hide.

The redesigned biography is drawn from the previous README. Numerical competitive-programming claims were replaced with links to the live profiles; project titles and technology stacks were retained. The old README remains available through git history.
