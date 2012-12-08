Name:		gkrellm
Version:	2.3.5
Release:	5
Summary:	Multiple stacked system monitors
License:	GPLv3+
Group:		Monitoring
URL:		http://gkrellm.net
Source0:	http://members.dslextreme.com/users/billw/gkrellm/%{name}-%{version}.tar.bz2
Source1:	gkrellm-themes.tar.bz2
Source2:	gkrellmd.init
Source3:	gkrellm-pt.po
Patch0:		gkrellm-2.3.5-fix-format-errors.patch
Patch2:		gkrellm-2.3.5-force-libsensor-test-result.patch
BuildRequires:	gettext
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(libntlm)
BuildRequires:	lm_sensors-devel

%description
GKrellM charts SMP CPU, load, Disk, and all active net interfaces
automatically. An on/off button and online timer for the PPP interface
is provided. Monitors for memory and swap usage, file system, internet
connections, APM laptop battery, mbox style mailboxes, and cpu temps.
Also includes an uptime monitor, a hostname label, and a clock/calendar.
Additional features are:

  * Autoscaling grid lines with configurable grid line resolution.
  * LED indicators for the net interfaces.
  * A gui popup for configuration of chart sizes and resolutions.

%package devel
Summary:	Include files for gkrellm
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
gkrellm header files for gkrellm development and plugin support.

%package server
Summary:	Server component for gkrellm
Group:		Monitoring
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description server
The server component allows you to monitor a server remotely from 
a client running gkrellm, without installing gkrellm on the server.

%prep
%setup -q
%setup -q -D -T -a1
cp -a %{S:3} po/pt.po
for i in `find -type d -name .xvpics`
    do rm -rf $i
done
# make it lib64 aware
perl -pi -e "/PLUGINS_DIR/ and s|/lib/|/%{_lib}/|g" ./src/gkrellm.h ./server/gkrellmd.h
perl -pi -e "s|/lib/|/%{_lib}/|" Makefile
%patch0 -p1 -b .wformat
%patch2 -p1 -b .libsensors

%build
%make INSTALLROOT=%{_prefix} \
      INCLUDEDIR=%{_includedir} \
      CFLAGS="%{optflags}" \
      LDFLAGS="$(pkg-config --libs gmodule-2.0) %{ldflags}" \
      LOCALEDIR=%{_datadir}/locale

#      LIBS="-lgtk-x11-2.0 -lgdk-x11-2.0 -lglib-2.0 -lgmodule-2.0"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
make install \
    INSTALLROOT=%{buildroot}%{_prefix} \
    INSTALLDIR=%{buildroot}%{_bindir} \
    INCLUDEDIR=%{buildroot}%{_includedir} \
    MANDIR=%{buildroot}%{_mandir}/man1 \
    LOCALEDIR=%{buildroot}%{_datadir}/locale \
    STRIP=""

mkdir -p %{buildroot}%{_libdir}/%{name}2/plugins

mkdir -p %{buildroot}{%{_iconsdir},%{_liconsdir},%{_miconsdir}}
convert src/icon.xpm -geometry 48x48 %{buildroot}%{_liconsdir}/%{name}.png
convert src/icon.xpm -geometry 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert src/icon.xpm -geometry 16x16 %{buildroot}%{_miconsdir}/%{name}.png

mkdir -p %{buildroot}%{_datadir}/%{name}2/themes
cp -av gkrellm-themes/* %{buildroot}%{_datadir}/%{name}2/themes

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Gkrellm
Comment=A GTK-based monitoring app
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;System;Monitor;
EOF

install -d -m 755 %{buildroot}%{_sysconfdir}
install -m 644 server/gkrellmd.conf %{buildroot}%{_sysconfdir}

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/gkrellmd

%multiarch_includes %{buildroot}%{_includedir}/gkrellm2/gkrellm.h

%multiarch_includes %{buildroot}%{_includedir}/gkrellm2/gkrellmd.h

%{find_lang} %{name}

# lock dir
install -d -m 755 %{buildroot}%{_localstatedir}/lock/gkrellm
chmod 1777 %{buildroot}%{_localstatedir}/lock/gkrellm

%post server
%_post_service gkrellmd

%preun server
%_preun_service gkrellmd

%files -f %{name}.lang
%doc COPYRIGHT Changelog INSTALL README *.html
%{_bindir}/gkrellm
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/gkrellm.png
%{_liconsdir}/gkrellm.png
%{_miconsdir}/gkrellm.png
%{_mandir}/man1/gkrellm.1*
%{_libdir}/gkrellm2
%{_datadir}/gkrellm2
%{_localstatedir}/lock/gkrellm

%files devel
%doc *.html
%{_includedir}/gkrellm2/
%dir %{multiarch_includedir}/gkrellm2
%{multiarch_includedir}/gkrellm2/*.h
%{_libdir}/pkgconfig/gkrellm.pc

%files server
%config(noreplace) %{_sysconfdir}/gkrellmd.conf
%{_initrddir}/gkrellmd
%{_bindir}/gkrellmd
%{_mandir}/man1/gkrellmd.1*


%changelog
* Tue Dec 06 2011 ZÃ© <ze@mandriva.org> 2.3.5-3
+ Revision: 738057
- clean useless macros
- 2009 is no longer maintained
- add PT translation
- clean defattr, BR, clean section and mkrel
- clean useless macros
- 2009 is no longer maintained
- add PT translation
- clean defattr, BR, clean section and mkrel

* Mon May 02 2011 Funda Wang <fwang@mandriva.org> 2.3.5-2
+ Revision: 662193
- update file list
- fix multiarch usage

  + Oden Eriksson <oeriksson@mandriva.com>
    - multiarch fixes

* Mon Oct 11 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.5-1mdv2011.0
+ Revision: 584908
- new version

* Thu Aug 12 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.4-10mdv2011.0
+ Revision: 569173
- force libsensor backend building, without running a test

* Fri May 07 2010 Funda Wang <fwang@mandriva.org> 2.3.4-9mdv2010.1
+ Revision: 543131
- fix gkrellm plugin loading by specify correct ldflags

* Tue May 04 2010 Funda Wang <fwang@mandriva.org> 2.3.4-8mdv2010.1
+ Revision: 542002
- should fix bug#58823 (missing binary symbols)

* Tue May 04 2010 Funda Wang <fwang@mandriva.org> 2.3.4-7mdv2010.1
+ Revision: 541983
- bunzip2 init file
- more linkage fix for gkrellmd
- BR ntlm

* Thu Apr 08 2010 Eugeni Dodonov <eugeni@mandriva.com> 2.3.4-6mdv2010.1
+ Revision: 533006
- Rebuild for new openssl

* Thu Apr 08 2010 Funda Wang <fwang@mandriva.org> 2.3.4-5mdv2010.1
+ Revision: 532879
- bump rel
- fix linkage

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.4-3mdv2010.1
+ Revision: 511569
- rebuilt against openssl-0.9.8m

* Sat Jan 09 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.4-2mdv2010.1
+ Revision: 487942
- add missing directory preventing multiple instances locking (fix #56907)

* Wed Jan 06 2010 Frederik Himpe <fhimpe@mandriva.org> 2.3.4-1mdv2010.1
+ Revision: 486869
- update to new version 2.3.4

* Wed Dec 30 2009 Frederik Himpe <fhimpe@mandriva.org> 2.3.3-1mdv2010.1
+ Revision: 484014
- Update to new version 2.3.3
- Remove getline patch: not needed anymore

* Wed Aug 12 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.3.2-3mdv2010.0
+ Revision: 415391
- add patch to fix compilation on 64 bit (getline is defined in stdio.h and was redefined)
- remove reference to bash completion sources
- fix -Wformat warnings

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - keep bash completion in its own package

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Sat Oct 11 2008 Frederik Himpe <fhimpe@mandriva.org> 2.3.2-1mdv2009.1
+ Revision: 291673
- update to new version 2.3.2

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 2.3.1-1mdv2009.0
+ Revision: 218423
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Dec 11 2007 Funda Wang <fwang@mandriva.org> 2.3.1-1mdv2008.1
+ Revision: 117372
- New version 2.3.1

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Thu Jul 26 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.0-1mdv2008.0
+ Revision: 55660
- update to new version 2.3.0

* Fri May 11 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.10-1mdv2008.0
+ Revision: 26290
- new version


* Fri Aug 04 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.9-4mdv2007.0
- xdg menu

* Fri Jun 23 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.9-3mdv2007.0
- buildrequires sm-devel

* Wed May 03 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.9-2mdk
- buildrequires openssl-devel

* Mon Apr 03 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.9-1mdk
- New release 2.2.9

* Sun Apr 02 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.8-1mdk
- New release 2.2.8

* Tue Dec 20 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.7-2mdk
- %%mkrel
- prereq -> requires

* Mon Jun 20 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.7-1mdk
- New release 2.2.7

* Mon Apr 25 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.5-1mdk 
- new release
- fix source URL

* Wed Mar 16 2005 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.2.4-4mdk
- fix the convert stuff
- fix rpmlint errors

* Mon Jan 31 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.2.4-3mdk 
- more multiarch fix
- spec cleanup

* Fri Jan 21 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.4-2mdk
- multiarch

* Thu Oct 28 2004 Guillaume Rousse <guillomovitch@mandrakesoft.com> 2.2.4-1mdk
- New release 2.2.4

* Thu Jul 22 2004 Guillaume Rousse <guillomovitch@mandrakesoft.com> 2.2.2-1mdk
- New release 2.2.2

* Fri Jun 11 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.2.1-1mdk 
- new version
- rpmbuildupdate aware

* Wed Mar 31 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.28-1mdk
- new version

* Thu Jan 22 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.25-2mdk
- build icon from sources (Charles A Edwards <eslrahc@bellsouth.net>)

* Thu Jan 22 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.25-1mdk
- new version

* Mon Jan 05 2004 Abel Cheung <deaddog@deaddog.org> 2.1.24-3mdk
- Remove bash-completion dependency

* Mon Dec 29 2003 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.24-2mdk
- added bash-completion
- bzipped additional sources

* Sat Dec 27 2003 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.24-1mdk
- new version

* Thu Dec 18 2003 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.23-1mdk
- new version

* Wed Dec 17 2003 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.22-1mdk
- new version

* Tue Nov 18 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.1.21-1mdk
- new version

* Wed Oct  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.16-2mdk
- lib64 fixes

* Thu Aug 21 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.1.16-1mdk
- 2.1.16

* Fri Aug 08 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.1.15-2mdk
- rebuild

* Wed Aug 06 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.1.15-1mdk
- 2.1.15

* Tue Jul 08 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.1.14-2mdk
- fix l10n - specify correct LOCALEDIR during build instead of default
  /usr/local/share/locale (Andrey Borzenkov <arvidjaar@mail.ru>)

* Mon Jun 30 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.1.14-1mdk
- 2.1.14

* Sat Jun 21 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.1.12-2mdk
- plugins dir is %%{_libdir}/gkrellm2
- spec cleanup

* Sat Jun 14 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.1.12-1mdk
- 2.1.12a
- use $RPM_OPT_FLAGS
- fix pkgconfig file
- get rid of .xvpics files
- fix unowned dirs

* Tue Apr  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.7a-3mdk
- Make it lib64 aware

* Thu Jan 30 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.7a-2mdk
- gkrellmd initscript is back (thanks to Buchan Milne)

* Thu Jan 30 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.7a-1mdk
- Release 2.1.7a

* Mon Jan 13 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.5-1mdk
- Release 2.1.5

* Wed Oct 16 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.0.4-2mdk
- rebuild

* Fri Oct 11 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.0.4-1mdk
- 2.0.4
- fix menu
- include gkrellmd manpage
- from bgmilne@linux-mandrake.com:
  - 2.0.0
  - BuildRequires pkgconfig, gtk+2-devel
  - Put binaries in bindir, not prefix/X11R6/bin
  - Add server package for gkrellmd

* Tue Sep  3 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.2.13-3mdk
- fix icons (re: Robby Stephenson)

* Wed Aug 21 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.2.13-2mdk
- remove language files from devel package (conflicts)

* Fri Aug 09 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.2.13-1mdk
- 1.2.13

* Tue Jul 16 2002 Stefan van der Eijk <stefan@eijk.nu> 1.2.11-2mdk
- BuildRequires

* Sat May 04 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.2.11-1mdk
- 1.2.11

* Sat Mar 02 2002 David BAUDENS <baudens@mandrakesoft.com> 1.2.8-2mdk
- Use monitoring_section.png for menu (so don't break E menu)
- Requires: %%version-%%release and not only %%version

* Thu Jan 31 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.2.8-1mdk
- 1.2.8
- include some themes as another source package and not in the gkrellm
  source package (bad)
- convert menu icons to png

* Wed Nov  7 2001 Sebastien Dupont <sdupont@mandrakesoft.com> 1.2.4-2mdk
- include some themes

* Wed Oct 31 2001 Sebastien Dupont <sdupont@mandrakesoft.com> 1.2.4-1mdk
- new version 1.2.4

* Wed Oct 31 2001 Sebastien Dupont <sdupont@mandrakesoft.com> 1.2.2-3mdk
- lang problems & doc

* Fri Oct 19 2001 Sebastien Dupont <sdupont@mandrakesoft.com> 1.2.2-2mdk
- License

* Sat Sep 29 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.2.2-1mdk
- 1.2.2
- include locales

* Thu Aug  9 2001 Stew Benedict <sbenedict@mandrakesoft.com> 1.2.1-1mdk
- 1.2.1 s/Copyright/License/ move plugins to /usr/lib/gkrellm for FHS

* Mon Apr 30 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.8-1mdk
- 1.0.8

* Wed Mar 14 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.7-1mdk
- 1.0.7

* Wed Jan 31 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.6-1mdk
- 1.0.6

* Tue Jan 23 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.5-1mdk
- 1.0.5

* Tue Jan 16 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.4-1mdk
- 1.0.4

* Sun Jan 07 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.3-1mdk
- 1.0.3

* Wed Nov 15 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.0.2-1mdk
- 1.0.2

* Mon Nov  6 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.0.1-2mdk
- rebuild for new libstdc++

* Thu Oct 20 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.0.1-1mdk
- 1.0.1

* Fri Oct 13 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.0.0-1mdk
- 1.0.0

* Fri Oct 06 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.10.5-3mdk
- added missing icons

* Tue Aug 08 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.10.5-2mdk
- automatically added BuildRequires

* Mon Aug 07 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.10.5-1mdk
- 0.10.5
- more macros
- added requires version for gkrellm-devel
- move include dir from /usr/X11R6/include to /usr/include

* Wed Jul 12 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.10.4-1mdk
- 0.10.4
- macroization
- move plugins to their own RPM
- add devel package

* Wed Jul 05 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.10.2-1mdk
- v 0.10.2

* Wed May 24 2000 Vincent Danen <vdanen@linux-mandrake.com> 0.9.10-1mdk
- 0.9.10
- bzip2 patches
- comment out all plugins since they refuse to compile

* Tue Apr 25 2000 Vincent Danen <vdanen@linux-mandrake.com> 0.9.8-1mdk
- 0.9.8
- Added gkrellmms plugin by Sander Lebbink <sander@cerberus.demon.nl>

* Mon Apr 10 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.9.7-1mdk
- fix group
- add menu entry

* Fri Mar 24 2000 Vincent Danen <vdanen@linux-mandrake.com>
- 0.9.7

* Sun Mar 12 2000 Vincent Danen <vdanen@linux-mandrake.com>
- 0.9.6
- Added seti@home plugin by Henry Palonen <henkka@yty.net>
- Added plugin to to display fan speeds by Jarkko Lietolahti <jappe@iki.fi>
- since plugins (currently) need to be in ~/.gkrellm/plugins, you must
  symlink to the plugins in /usr/share/gkrellm/plugins

* Fri Mar 3 2000 Vincent Danen <vdanen@linux-mandrake.com>
- 0.9.5

* Mon Feb 28 2000 Vincent Danen <vdanen@linux-mandrake.com>
- 0.9.4
- libgtop is no longer required

* Thu Feb 24 2000 Vincent Danen <vdanen@linux-mandrake.com>
- 0.9.3

* Wed Feb 23 2000 Vincent Danen <vdanen@linux-mandrake.com>
- 0.9.1

* Tue Feb 22 2000 Vincent Danen <vdanen@linux-mandrake.com>
- 0.9.0
- libgtop-devel is now required but it seems to be broken as the
  glibtop-config.h is in /usr/lib/libgtop/include and not /usr/include/ like
  it should be (you must manually copy before building the RPM)

* Sun Feb 13 2000 Vincent Danen <vdanen@linux-mandrake.com>
- 0.8.1

* Mon Dec 06 1999 Lenny Cartier <lenny@mandrakesoft.com>
- 0.7.5

* Fri Nov 19 1999 Lenny Cartier <lenny@mandrakesoft.com>
- New in contrib
- Used the SRPMS provided by Vincent Danen
- bz2 archive
- 0.7.4

* Wed Nov 17 1999 Vincent Danen <vdanen@linux-mandrake.com>
- updated specfile for Mandrake contribution

* Thu Nov 11 1999 Vincent Danen <vdanen@softhome.net>
- wrote spec file
- 0.7.3
