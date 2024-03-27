%bcond_without  base
%bcond_without  next
%bcond_without  openh264
%bcond_with     modular
%bcond_with     playground

Name:           epel-release
Version:        9
Release:        7%{dist}
Summary:        Extra Packages for Enterprise Linux repository configuration
License:        GPLv2

# This is a EPEL maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
URL:            http://download.fedoraproject.org/pub/epel
Source0:        http://download.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-%{version}
Source1:        GPL

Source100:      epel.repo
Source101:      epel-next.repo
Source102:      epel-modular.repo
Source103:      epel-playground.repo
Source104:      epel-cisco-openh264.repo

Source200:      epel-testing.repo
Source201:      epel-next-testing.repo
Source202:      epel-testing-modular.repo

# EPEL default preset policy (borrowed from fedora's 90-default.preset)
Source300:      90-epel.preset

# Add epel crb repo
Source301:      crb

BuildArch:      noarch
Requires:       redhat-release >=  %{version}
# epel-release is only for enterprise linux, not fedora
Conflicts:      fedora-release
# crb needs config-manager to run
# But only recommend it, incase people do not need crb
Recommends:     dnf-command(config-manager)
%if %{with next}
Recommends:     (epel-next-release if centos-stream-release)
%endif


%description
This package contains the Extra Packages for Enterprise Linux (EPEL) repository
GPG key as well as configuration for yum.


%if %{with next}
%package -n epel-next-release
Summary:        Extra Packages for Enterprise Linux Next repository configuration
Requires:       %{name} = %{version}-%{release}


%description -n epel-next-release
This package contains the Extra Packages for Enterprise Linux (EPEL) Next
configuration for yum.
%endif


%prep
%setup -q -c -T
install -pm 644 %{SOURCE1} .


%install
# GPG Key
install -Dpm 644 %{SOURCE0} \
    %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL-%{version}

# yum repo configs
install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
%if %{with base}
install -pm 644 %{SOURCE100} %{SOURCE200} %{buildroot}%{_sysconfdir}/yum.repos.d
%endif
%if %{with next}
install -pm 644 %{SOURCE101} %{SOURCE201} %{buildroot}%{_sysconfdir}/yum.repos.d
%endif
%if %{with modular}
install -pm 644 %{SOURCE102} %{SOURCE202} %{buildroot}%{_sysconfdir}/yum.repos.d
%endif
%if %{with playground}
install -pm 644 %{SOURCE103} %{buildroot}%{_sysconfdir}/yum.repos.d
%endif
%if %{with openh264}
install -pm 644 %{SOURCE104} %{buildroot}%{_sysconfdir}/yum.repos.d
%endif

# systemd presets
install -pm 644 -D %{SOURCE300} %{buildroot}%{_prefix}/lib/systemd/system-preset/90-epel.preset

# Add epel crb repo
install -D -pm744 -t %{buildroot}%{_bindir} %{SOURCE301}

%post
# Doing a check to see if crb is enabled is as hard and resource intense as enabling or disabling crb.
#   So we will say crb is recommended, without first checking.  But only on the initial install.
if [ "$1" -eq 1 ] ; then
  echo "Many EPEL packages require the CodeReady Builder (CRB) repository."
  echo "It is recommended that you run %{_bindir}/crb enable to enable the CRB repository."
fi


%files
%license GPL
%if %{with base}
%config(noreplace) %{_sysconfdir}/yum.repos.d/epel.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/epel-testing.repo
%endif
%if %{with modular}
%config(noreplace) %{_sysconfdir}/yum.repos.d/epel-modular.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/epel-testing-modular.repo
%endif
%if %{with playground}
%config(noreplace) %{_sysconfdir}/yum.repos.d/epel-playground.repo
%endif
%if %{with openh264}
%config(noreplace) %{_sysconfdir}/yum.repos.d/epel-cisco-openh264.repo
%endif
%{_sysconfdir}/pki/rpm-gpg/*
%{_prefix}/lib/systemd/system-preset/90-epel.preset
%{_bindir}/crb

%if %{with next}
%files -n epel-next-release
%config(noreplace) %{_sysconfdir}/yum.repos.d/epel-next.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/epel-next-testing.repo
%endif


%changelog
* Thu Aug 17 2023 Neal Gompa <ngompa@fedoraproject.org> - 9-7
- Fix typo to actually enable EPEL OpenH264 repo

* Tue Aug 15 2023 Neal Gompa <ngompa@fedoraproject.org> - 9-6
- Add EPEL OpenH264 repository (#2053295)

* Fri Apr 14 2023 Troy Dawson <tdawson@redhat.com> - 9-5
- Tweak crb script, check os-release for RHEL (#2186721)

* Tue Aug 09 2022 Troy Dawson <tdawson@redhat.com> - 9-4
- Tweak crb script, Recommends dnf-command(config-manager) (#2115602)

* Wed Jun 29 2022 Troy Dawson <tdawson@redhat.com> - 9-3
- Add crb script

* Wed Dec 01 2021 Carl George <carl@george.computer> - 9-2
- Enable epel9 repo files

* Fri Oct 08 2021 Carl George <carl@redhat.com> - 9-1
- Initial package for epel9-next

* Fri Sep 03 2021 Mohan Boddu <mboddu@bhujji.com> - 8-13
- Change the baseurl to point to source/tree for srpms

* Fri Jul 30 2021 Kevin Fenzi <kevin@scrye.com> - 8-12
- Enable certbot-renew.timer ( rhbz#1986205 )

* Thu Jun 03 2021 Carl George <carl@george.computer> - 8-11
- Add epel-next-release subpackage

* Sat Dec 05 2020 Kevin Fenzi <kevin@scrye.com> - 8-10
- Add x509watch.timer enabled by default. Fixes bug #1901721

* Sat Oct 31 2020 Kevin Fenzi <kevin@scrye.com> - 8-9
- Add countme feature for epel. Fixes bug #1825984

* Fri Dec 13 2019 Merlin Mathesius <mmathesi@redhat.com> - 8-8%{dist}
- Add modular repos.

* Thu Oct 10 2019 Stephen Smoogen <smooge@fedoraproject.org> - 8-7%{dist}
- Remove failovermethod from EPEL8 tree. It is no longer needed.

* Mon Sep 16 2019 Stephen Smoogen <smooge@fedoraproject.org> - 8-6%{dist}
- Change gpg key to use -8 versus -$releasever. This fixes bash problem

* Tue Aug  6 2019 Stephen Smoogen <smooge@fedoraproject.org> - 8-5%{dist}
- Fix playground release to have os/ on its name [Kevin Fenzi]
- Make sure all values of $release are $releasever


* Thu Aug  1 2019 Pablo Greco <pgreco@centosproject.org> - 8-4
- Use the correct var for dnf to expand
- Update playground source url
- Remove epel-modules repo
- Use https in baseurl

* Thu Aug  1 2019 Stephen Smoogen <smooge@fedoraproject.org> - 8-3
- Make sure that the key name is named correctly

* Thu Aug  1 2019 Stephen Smoogen <smooge@fedoraproject.org> - 8-2
- Make baseurl paths match dl.fedoraproject.org
- Add draft of epel8 packaging
- Fix docs

* Thu Jul 18 2019 Stephen Smoogen <smooge@smoogen-laptop.localdomain> - 8-1
- Update for RHEL-8
- Add playground repo data
- Clean out 90-epel.preset to make sure we dont override RHEL-8 items. Just add items in which EPEL needs.

* Mon Oct 02 2017 Kevin Fenzi <kevin@scrye.com> - 7-11
- Add Conflicts on fedora-release to prevent people from installing on Fedora systems. Fixes bug #1497702

* Sat Jun 24 2017 Kevin Fenzi <kevin@scrye.com> - 7-10
- Change mirrorlist= in repo files to be metalink= (as thats what they are). Fixes bug #1451212

* Tue Dec 27 2016 Kevin Fenzi <kevin@scrye.com> - 7-9
- Add preset for drbdlinks package. Fixes bug #1405744

* Sat Jul 23 2016 Kevin Fenzi <kevin@scrye.com> - 7-8
- Drop duplicate libstoragemgmt from presets. Fixes bug #1358971

* Fri Jun 03 2016 Kevin Fenzi <kevin@scrye.com> - 7-7
- Drop initial-setup from presets. Fixes bug #1342511

* Wed Mar 30 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 7-6
- Remove macros.epel; let epel-rpm-macros handle it instead.

* Tue Nov 25 2014 Rex Dieter <rdieter@fedoraproject.org> 7-5
- fix typo in macros.epel

* Fri Nov 21 2014 Rex Dieter <rdieter@fedoraproject.org> 7-4
- add systemd 90-epel.preset

* Fri Nov 21 2014 Rex Dieter <rdieter@fedoraproject.org> 7-3
- implement %%epel macro

* Tue Sep 02 2014 Kevin Fenzi <kevin@scrye.com> 7-2
- Make repo files config(noreplace). Fixes bug #1135576

* Thu Aug 28 2014 Dennis Gilmore <dennis@ausil.us> - 7-1
- enable gpg checking now we are out of beta

* Wed Jun 18 2014 Kevin Fenzi <kevin@scrye.com> 7-0.2
- Drop unneeded up2date post/postun
- Fixed up description.
- Fixes bugs #1052434 and #1093918

* Mon Dec 16 2013 Dennis Gilmore <dennis@ausil.us> - 7-0.1
- initial epel 7 build. gpg cheking is disabled

