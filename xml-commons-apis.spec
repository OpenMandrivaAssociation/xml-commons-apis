%{?_javapackages_macros:%_javapackages_macros}
%if 0%{?fedora}
%else
# FIXME mandriva has an epoch..
Epoch:         1
%endif
Name:          xml-commons-apis
Version:       1.4.01
Release:       18.1
Summary:       APIs for DOM, SAX, and JAXP
Group:         Development/Java
License:       ASL 2.0 and W3C and Public Domain
URL:           http://xml.apache.org/commons/

# From source control because the published tarball doesn't include some docs:
#   svn export http://svn.apache.org/repos/asf/xml/commons/tags/xml-commons-external-1_4_01/java/external/
#   tar czf xml-commons-external-1.4.01-src.tar.gz external
Source0:       xml-commons-external-%{version}-src.tar.gz
Source1:       %{name}-MANIFEST.MF
Source2:       %{name}-ext-MANIFEST.MF
Source3:       http://repo1.maven.org/maven2/xml-apis/xml-apis/2.0.2/xml-apis-2.0.2.pom
Source4:       http://repo1.maven.org/maven2/xml-apis/xml-apis-ext/1.3.04/xml-apis-ext-1.3.04.pom

BuildArch:     noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils
BuildRequires: ant
BuildRequires: zip
Requires:      java
Requires:      jpackage-utils

Obsoletes:     xml-commons < %{version}-%{release}
Provides:      xml-commons = %{version}-%{release}

# TODO: Ugh, this next line should be dropped since it actually provides JAXP 1.4 now...
Provides:      xml-commons-jaxp-1.3-apis = %{version}-%{release}

%description
xml-commons-apis is designed to organize and have common packaging for
the various externally-defined standard interfaces for XML. This
includes the DOM, SAX, and JAXP.

%package manual
Summary:       Manual for %{name}


%description manual
%{summary}.

%package javadoc
Summary:       Javadoc for %{name}


%description javadoc
%{summary}.

%prep
%setup -q -n external
# Make sure upstream hasn't sneaked in any jars we don't know about
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

# Fix file encodings
iconv -f iso8859-1 -t utf-8 LICENSE.dom-documentation.txt > \
  LICENSE.dom-doc.temp && mv -f LICENSE.dom-doc.temp LICENSE.dom-documentation.txt
iconv -f iso8859-1 -t utf-8 LICENSE.dom-software.txt > \
  LICENSE.dom-sof.temp && mv -f LICENSE.dom-sof.temp LICENSE.dom-software.txt

# remove bogus section from poms
cp %{SOURCE3} %{SOURCE4} .
sed -i '/distributionManagement/,/\/distributionManagement/ {d}' *.pom

%build
ant -Dant.build.javac.source=1.5 -Dant.build.javac.target=1.5 jar javadoc

%install
# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/xml-apis.jar META-INF/MANIFEST.MF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/xml-apis-ext.jar META-INF/MANIFEST.MF

# Jars
install -pD -T build/xml-apis.jar %{buildroot}%{_javadir}/%{name}.jar
install -pDm 644 xml-apis-[0-9]*.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap -a xerces:dom3-xml-apis

install -pD -T build/xml-apis-ext.jar %{buildroot}%{_javadir}/%{name}-ext.jar
install -pDm 644 xml-apis-ext*.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}-ext.pom
%add_maven_depmap JPP-%{name}-ext.pom %{name}-ext.jar

# for better interoperability with the jpp apis packages
ln -sf %{name}.jar %{buildroot}%{_javadir}/jaxp13.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/jaxp.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/xml-commons-jaxp-1.3-apis.jar

# Javadocs
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr build/docs/javadoc/* %{buildroot}%{_javadocdir}/%{name}

# prevent apis javadoc from being included in doc
rm -rf build/docs/javadoc

%files -f .mfiles
%doc LICENSE NOTICE
%doc LICENSE.dom-documentation.txt README.dom.txt
%doc LICENSE.dom-software.txt LICENSE.sac.html
%doc LICENSE.sax.txt README-sax  README.sax.txt
%{_javadir}/*

%files manual
%doc build/docs/*

%files javadoc
%{_javadocdir}/*

%changelog
* Tue Aug 6 2013 Krzysztof Daniel <kdaniel@redhat.com> 1.4.01-14
- Fix FTBFS.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.01-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Krzysztof Daniel <kdaniel@redhat.com> 1.4.01-12
- Update manifest to match Eclipse version (Resolved: rhbz#964039).

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.01-11
- Add Require-Bundle: system.bundle to manifest
- Resolves: rhbz#917659

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov  2 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.01-9
- Add additional maven depmap

* Fri Aug 17 2012 Andy Grimm <agrimm@gmail.com> - 1.4.01-8
- Remove osgi(system.bundle) requirement from manifest

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 21 2011 Orion Poplawski <orion@cora.nwra.com> - 1.4.01-5
- Add missing packages to manifest - javax.xml.stream, javax.xml.stream.events,
  javax.xml.stream.util, javax.xml.transform.stax (bug #743360)

* Fri May  6 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.01-4
- Add maven metadata
- Few guidelines tweaks (buildroot, clean, defattr)
- Versionless jars & javadocs

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Mat Booth <fedora@matbooth.co.uk> 1.4.01-2
- Fix FTBFS and rpmlint warnings.
- Don't package javadoc in manual package.

* Sat Jan 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.01-1
- Update to 1.4.01.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.04-3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.04-2.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 6 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.3.04-1.5
- Add osgi metadata to the ext jar too.

* Fri Jan 30 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.3.04-1.4
- Add osgi metadata.

* Fri Sep 19 2008 Matt Wringe <mwringe@redhat.com> - 0:1.3.04-1.3
- Remove natively compiled bits from the javadoc package (462809)

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.3.04-1.2
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.3.04-1jpp.1
- Autorebuild for GCC 4.3

* Tue Mar 06 2007 Matt Wringe <mwringe@redhat.com> - 0:1.3.04-0jpp.1
- Update to 1.3.04

* Tue Mar 06 2007 Matt Wringe <mwringe@redhat.com> - 0:1.3.03-0jpp.1
- Split xml-commons package up into 2 separate package: xml-commons-apis
  and xml-commons-which.

* Mon Aug 21 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.3.02-0.b2.7jpp.10
- Add missing Requires for post and postun javadoc sections

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.3.02-0.b2.7jpp_9fc
- Rebuilt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.3.02-0.b2.7jpp_8fc
- rebuild

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:1.3.02-0.b2.7jpp_7fc
- stop scriptlet spew

* Wed Feb 22 2006 Rafael Schloming <rafaels@redhat.com> - 0:1.3.02-0.b2.7jpp_6fc
- Updated to 1.3

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:1.0-0.b2.7jpp_5fc
- bump again for double-long bug on ppc(64)

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> 0:1.0-0.b2.7jpp_4fc
- rebuilt again

* Tue Dec 13 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Jul 15 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.7jpp_3fc
- Build on ia64, ppc64, s390 and s390x.
- Switch to aot-compile-rpm (also BC-compiles the which jar).

* Wed Jun 15 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.7jpp_2fc
- Remove all prebuilt stuff from the tarball.

* Thu May 26 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.7jpp_1fc
- Upgrade to 1.0-0.b2.7jpp.
- Remove now-unnecessary workaround for #130162.
- Rearrange how BC-compiled stuff is built and installed.

* Mon May 23 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.6jpp_13fc
- Add alpha to the list of build architectures (#157522).
- Use absolute paths for rebuild-gcj-db.

* Thu May  5 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.6jpp_12fc
- Add dependencies for %%post and %%postun scriptlets (#156901).

* Tue May  3 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.6jpp_11fc
- BC-compile the API jar.

* Tue Apr 26 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.6jpp_10fc
- Remove gcj endorsed dir support (#155693).

* Mon Apr 25 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.6jpp_9fc
- Provide a default transformer when running under libgcj.

* Mon Apr 25 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.6jpp_8fc
- Provide a default DOM builder when running under libgcj (#155693).

* Fri Apr 22 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.6jpp_7fc
- Provide a default SAX parser when running under libgcj (#155693).

* Thu Apr 21 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.6jpp_6fc
- Add gcj endorsed dir support.

* Tue Jan 11 2005 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.6jpp_5fc
- Sync with RHAPS.

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.6jpp_4fc
- Build into Fedora.

* Thu Oct 28 2004 Gary Benson <gbenson@redhat.com> - 0:1.0-0.b2.6jpp_3fc
- Bootstrap into Fedora.

* Fri Oct 1 2004 Andrew Overholt <overholt@redhat.com> - 0:1.0-0.b2.6jpp_3rh
- add coreutils BuildRequires

* Thu Mar  4 2004 Frank Ch. Eigler <fche@redhat.com> - 0:1.0-0.b2.6jpp_2rh
- RH vacuuming part II

* Tue Mar  2 2004 Frank Ch. Eigler <fche@redhat.com> - 0:1.0-0.b2.6jpp_1rh
- RH vacuuming
